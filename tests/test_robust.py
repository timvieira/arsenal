from time import sleep, time

from arsenal.assertions import assert_throws
from arsenal.robust import retry, retry_apply, timelimit, Timeout


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
        retry_apply(f, (10,), tries=2)

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
