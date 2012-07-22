import sys
import time
from threading import Thread
from functools import wraps

# TODO: add verbose argument to timelimit and retry

class dispatch(Thread):
    def __init__(self, f, *args, **kwargs):
        Thread.__init__(self)
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.error = None
        self.setDaemon(True)
        self.start()
    def run(self):
        try:
            self.result = self.f(*self.args, **self.kwargs)
        except:
            # store exception information in the thread.
            self.error = sys.exc_info()

class TimeoutError(Exception):
    pass

def timelimit(timeout):
    """
    A decorator to limit a function to `timeout` seconds, raising TimeoutError
    if it takes longer.

        >>> def meaningoflife():
        ...     time.sleep(.2)
        ...     return 42
        >>>
        >>> timelimit(.1)(meaningoflife)()
        Traceback (most recent call last):
            ...
        TimeoutError: took too long
        >>> timelimit(1)(meaningoflife)()
        42

    _Caveat:_ The function isn't stopped after `timeout` seconds but continues
    executing in a separate thread. (There seems to be no way to kill a thread)
    inspired by
        <http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473878>
    """
    def _1(f):
        @wraps(f)
        def _2(*args, **kwargs):
            c = dispatch(f, *args, **kwargs)
            c.join(timeout)
            if c.isAlive():
                raise TimeoutError('took too long')
            if c.error:
                raise c.error[1]
            return c.result
        return _2
    return _1

#_______________________________________________________________________________
#

def retry_apply(fn, args, kwargs=None, tries=2, pause=0.1, suppress=(Exception,),
                allow=(NameError, NotImplementedError)):
    """
    Attempt to call `fn` up to `tries` times with the `args` as arguments

    `suppress`: exceptions to be ignored up to the last retry-attempt.
    `allow`:    exceptions which will not be suppressed; this helps avoid
                stupid mistakes such as NameErrors and NotImplementedErrors.
    """
    for i in xrange(tries):
        try:
            return fn(*args, **(kwargs or {}))
        except allow:          # raise these exceptions
            raise
        except suppress:
            if i == tries - 1:  # the last iteration
                raise
        time.sleep(pause)


def retry(tries=2, pause=0.1, suppress=(Exception,), allow=(NameError, NotImplementedError)):
    def retry1(f):
        @wraps(f)
        def retry2(*args, **kw):
            return retry_apply(f, args, kw, tries=tries, pause=pause, suppress=suppress, allow=allow)
        return retry2
    return retry1


if __name__ == '__main__':
    from testing.assertions import assert_throws

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
            print retry_apply(f, (10,), tries=2)


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


    def test_timed():

        @timelimit(1.0)
        def sleepy_function(x): time.sleep(x)

        with assert_throws(TimeoutError):
            sleepy_function(3.0)

        sleepy_function(0.2)

        @timelimit(1)
        def raises_errors(): return 1/0
        with assert_throws(ZeroDivisionError):
            raises_errors()

    test_retry()
    test_timed()

    import doctest
    doctest.testmod()

    print 'passed tests..'
