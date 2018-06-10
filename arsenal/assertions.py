
class assert_throws(object):
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

    """

    def __init__(self, *expect):
        self.expect = expect
        super(assert_throws, self).__init__()

    def __enter__(self, *_):
        pass

    def __exit__(self, exc, val, _):
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

        with assert_throws(Exception):
            print(1/0)

        with assert_throws(ZeroDivisionError):
            print(1/0)

        with assert_throws(None):
            pass

        try:
            with assert_throws(ZeroDivisionError, TypeError, ValueError):
                pass
        except AssertionError:
            pass
        else:
            raise AssertionError('test failed.')

        print('Passed basic tests.')

    test()
