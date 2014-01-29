

## IDEA: Maybe we can extend the awesome contextlib.contextmanager decorator:
## 
## from contextlib import GeneratorContextManager
## 
## This is a broken first attempt:
## def contextmanager2(f):
## 
##     @wraps(f)
##     def helper(decorated_f=None):
## 
##         class xx(GeneratorContextManager):
##             def __call__(self, *args, **kw):
##                 with self:
##                     return decorated_f(*args, **kw)
## 
##         return xx(f())
## 
##     return helper
## 
## @contextmanager2
## def preserve_cwd():
##     """
##     context-manager which doubles as a decorator that preserve current
##     working directory.
## 
##     Usage example:
## 
##     As a decorator:
##         >>> before = os.getcwd()
##         >>> @preserve_cwd
##         ... def foo():
##         ...     os.chdir('..')
##         >>> before == os.getcwd()
##         True
## 
##     As a context-manager:
##         >>> before = os.getcwd()
##         >>> with preserve_cwd():
##         ...     os.chdir('..')
##         >>> before == os.getcwd()
##         True
##     """
##     cwd = os.getcwd()
##     yield
##     os.chdir(cwd)


__all__ = ['ContextDecorator']

from functools import wraps

class ContextDecorator(object):
    """
    Create objects that act as both context managers *and* as decorators, and
    behave the same in both cases.

    This implementation of ContextDecorator is based on Michael Foord's
    http://pypi.python.org/pypi/contextdecorator.

    Original copyright / license:
      # Copyright (C) 2007-2010 Michael Foord
      # E-mail: michael AT voidspace DOT org DOT uk
      # http://pypi.python.org/pypi/contextdecorator
    """

    def before(self):
        """
        Called on entering the with block or starting the decorated function.

        If used in a with statement whatever this method returns will be the
        context manager.
        """
        return self

    def after(self, exc_type, exc_value, traceback):
        """
        Called on exit. Arguments and return value of this method have
        the same meaning as the __exit__ method of a normal context
        manager.

        Note: If the after method of was triggered by an exception, and we wish
        to prevent the exception from being propagated, this method it should
        return a true value. Otherwise, the exception will be processed
        normally (do not reraise the exception here!).
        """
        return False

    def __call__(self, f):
        @wraps(f)
        def inner(*args, **kw):
            with self:
                return f(*args, **kw)
        return inner

    def __enter__(self):
        return self.before()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.after(exc_type, exc_value, traceback)



#______________________________________________________________________________
# Unit tests

import unittest

class mycontext(ContextDecorator):
    started = False
    exc = None
    catch = False

    def before(self):
        self.started = True
        return self

    def after(self, exc_type, exc_val, tb):
        self.exc = exc_type
        return self.catch

class TestContext(unittest.TestCase):

    def test_context(self):
        context = mycontext()
        self.assertFalse(context.started)

        with context as result:
            self.assertTrue(result is context)
            self.assertTrue(context.started)

        with mycontext() as result:
            self.assertTrue(isinstance(context, mycontext))
            self.assertTrue(context.started)

    def test_exceptions(self):

        class MyException(Exception): pass

        @mycontext()
        def test():
            raise MyException()

        # assert raises MyException
        try:
            with mycontext():
                raise MyException()
        except MyException:
            pass
        else:
            self.assertTrue(False)

        # assert raises MyException
        try:
            test()
        except MyException:
            pass
        else:
            self.assertTrue(False)

    def test_decorator(self):

        @mycontext()
        def test(a,b,c):
            "my doc string"
            return (a,b,c)

        A,B,C = 'A','B','C'
        a,b,c = test(A,B,C)
        assert a is A and b is B and c is C
        assert test.__name__ == 'test'
        assert test.__doc__ == 'my doc string'

    def test_decorating_method(self):

        class Test(object):

            def __init__(self):
                self.a, self.b, self.c = "ABC"

            @mycontext()
            def method(self, a, b, c=None):
                self.a = a
                self.b = b
                self.c = c

        test = Test()
        test.method(1, 2)
        self.assertEqual(test.a, 1)
        self.assertEqual(test.b, 2)
        self.assertEqual(test.c, None)

        test.method('a', 'b', 'c')
        self.assertEqual(test.a, 'a')
        self.assertEqual(test.b, 'b')
        self.assertEqual(test.c, 'c')


if __name__ == '__main__':
    unittest.main()
    import doctest
    doctest.testmod()
