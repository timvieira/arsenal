import sys
from time import sleep, time
from threading import Thread
from functools import wraps
from contextlib import contextmanager

# Warning: signal is apparently unavailable on windows.
import signal

class Timeout(Exception): pass


@contextmanager
def timelimit(seconds, sig=signal.SIGALRM):
    """
    A decorator to limit a function to `timeout` seconds, raising `Timeout`.
    if it takes longer.

    >>> def meaningoflife():
    ...     sleep(.2)
    ...     return 42
    >>>
    >>> timelimit(.1)(meaningoflife)()
    Traceback (most recent call last):
        ...
    arsenal.robust.Timeout: Call took longer than 0.1 seconds.
    >>> timelimit(1)(meaningoflife)()
    42

    >>> with timelimit(.2):
    ...     sleep(1)
    Traceback (most recent call last):
        ...
    arsenal.robust.Timeout: Call took longer than 0.2 seconds.

    >>> with timelimit(.2):
    ...     sleep(.1)
    ...     print('finished')
    finished

    """
    if seconds is None:
        yield
        return

    def signal_handler(signum, frame):
        raise Timeout(f'Call took longer than {seconds} seconds.')

    old_handler = signal.signal(sig, signal_handler)
    old_timer = signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, *old_timer)
        signal.signal(sig, old_handler)

timelimit.Timeout = Timeout

#_______________________________________________________________________________
#

def retry_apply(fn, args, kwargs=None, tries=2, pause=None, suppress=(Exception,),
                allow=(NameError, NotImplementedError)):
    """
    Attempt to call `fn` up to `tries` times with the `args` as arguments

    `suppress`: exceptions to be ignored up to the last retry-attempt.
    `allow`:    exceptions which will not be suppressed; this helps avoid
                stupid mistakes such as NameErrors and NotImplementedErrors.
    """
    if kwargs is None:
        kwargs = {}
    for i in range(tries):
        try:
            return fn(*args, **kwargs)
        except allow:          # raise these exceptions
            raise
        except suppress:
            if i == tries - 1:  # the last iteration
                raise
        if pause is not None: sleep(pause)


def retry(tries=2, pause=None, suppress=(Exception,), allow=(NameError, NotImplementedError)):
    def retry1(f):
        @wraps(f)
        def retry2(*args, **kw):
            return retry_apply(f, args, kw, tries=tries, pause=pause, suppress=suppress, allow=allow)
        return retry2
    return retry1

