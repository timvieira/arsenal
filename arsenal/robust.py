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
    Timeout: Call took longer than 0.1 seconds.
    >>> timelimit(1)(meaningoflife)()
    42

    >>> with timelimit(.2):
    ...     sleep(1)
    Traceback (most recent call last):
        ...
    Timeout: Call took longer than 0.2 seconds.

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

    signal.signal(sig, signal_handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    yield
    signal.setitimer(signal.ITIMER_REAL, 0)   # disables alarm

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


if __name__ == '__main__':
    from arsenal.assertions import assert_throws

    def test_retry():

        class NotCalledEnough(Exception): pass
        class TroublsomeFunction(object):
            "Function-like object which must be called >=4 times before succeeding."
            def __init__(self):
                self.tries = 0
            def __call__(self, *args):
                self.tries += 1
                if self.tries > 4:
                    return True
                else:
                    raise NotCalledEnough

        f = TroublsomeFunction()
        assert retry_apply(f, (1,2,3), tries=5)
        assert f.tries == 5

        with assert_throws(NotCalledEnough):
            f = TroublsomeFunction()
            print(retry_apply(f, (10,), tries=2))


        def create_trouble(tries_needs, attempts):
            calls = []
            @retry(tries=attempts, pause=0.0)
            def troublesome(a, kw=None):
                "I'm a troublesome function!"
                assert a == 'A' and kw == 'KW'
                calls.append(1)
                if len(calls) < tries_needs:
                    raise NotCalledEnough
                else:
                    return 'the secret'
            assert troublesome.__doc__ == "I'm a troublesome function!"
            assert troublesome.__name__ == 'troublesome'
            troublesome('A', kw='KW')

        create_trouble(4, 4)

        with assert_throws(NotCalledEnough):
            create_trouble(4, 2)


        @retry(tries=4, pause=0.0)
        def broken_function():
            raise NotImplementedError

        with assert_throws(NotImplementedError):
            broken_function()

        print('retry tests: pass')


    def test_timed():

        @timelimit(1.0)
        def sleepy_function(x): sleep(x)

        with assert_throws(Timeout):  # should timeout
            sleepy_function(3.0)

        sleepy_function(0.2)   # should succeed

        @timelimit(1)
        def raises_errors(): return 1/0
        with assert_throws(ZeroDivisionError):
            raises_errors()

        with timelimit(.2):
            sleep(.01)
            print('finished')

        tic = time()
        lim = .2
        with assert_throws(Timeout):
            with timelimit(lim):
                sleep(lim + 1)
        toc = time()
        took = toc - tic
        # make sure we wait at least `lim`.
        assert took > lim
        # make sure that there isn't too much overhead
        assert abs(lim - took) < 0.001, abs(lim - took)
        print('decorator tests: pass')

    test_retry()
    test_timed()

    import doctest
    doctest.testmod(verbose=True)

    print('passed tests..')
