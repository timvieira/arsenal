## from contextlib import contextmanager
## from functools import wraps
##
## @contextmanager
## def assert_throws_ctx(*exc):
##     passed = False
##     got = None
##     try:
##         yield
##     except exc:
##         passed = True
##     except Exception as e:
##         got = e
##     else:
##         # since None isn't realy an exception, we have to special case it.
##         if None in exc:
##             passed = True
##     finally:
##         if not passed:
##             msg = ' or '.join(e.__name__ if e is not None else 'None' for e in exc)
##             raise AssertionError('did not raise required %s. Got %s instead.' % (msg, got))
##
## def assert_throws_dec(exc):
##     def wrap(f):
##         @wraps(f)
##         def wrap2(*args,**kw):
##             with assert_throws_ctx(exc):
##                 return f(*args,**kw)
##         return wrap2
##     return wrap


from arsenal.recipes.contextdecorator import ContextDecorator

class assert_throws(ContextDecorator):
    """
    Contextmanager + Decorator for asserting that a certain exceptions (or no
    exception) will arise with it's context.

    As a context manager:

      >>> with assert_throws(ZeroDivisionError):
      ...     1/0

      >>> with assert_throws(None):
      ...     pass

      >>> with assert_throws(None, ZeroDivisionError):
      ...     pass

      >>> with assert_throws(ZeroDivisionError):
      ...     pass
      Traceback (most recent call last):
          ...
      AssertionError: did not raise required ZeroDivisionError. Got None instead.

      >>> with assert_throws(AssertionError, ZeroDivisionError):
      ...     pass
      Traceback (most recent call last):
          ...
      AssertionError: did not raise required AssertionError or ZeroDivisionError. Got None instead.

    As a decorator:

      >>> @assert_throws(ZeroDivisionError)
      ... def foo():
      ...     1 + 1   # should not raise ZeroDivisionError
      ...
      >>> foo()
      Traceback (most recent call last):
          ...
      AssertionError: did not raise required ZeroDivisionError. Got None instead.
    """

    def __init__(self, *expect):
        self.expect = expect
        super(assert_throws, self).__init__()

    def after(self, exc, val, _):
        msg = ' or '.join('None' if e is None else e.__name__ for e in self.expect)

        if exc is None:
            if None not in self.expect:
                raise AssertionError('did not raise required %s. Got %s instead.' % (msg, None))
        else:
            if not issubclass(exc, self.expect):
                raise AssertionError('did not raise required %s. Got %s instead.' % (msg, exc.__name__))

        return True


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    def test():

        @assert_throws(ZeroDivisionError)
        def test_assert_throws1():
            return 1/0
        test_assert_throws1()

        @assert_throws(None)
        def test_assert_throws2():
            return 2 + 2
        test_assert_throws2()

        with assert_throws(Exception):
            print 1/0

        with assert_throws(ZeroDivisionError):
            print 1/0

        with assert_throws(None):
            pass

        try:
            with assert_throws(ZeroDivisionError, TypeError, ValueError):
                pass
        except AssertionError:
            pass
        else:
            raise AssertionError('test failed.')

        print 'Passed basic tests.'

    test()
