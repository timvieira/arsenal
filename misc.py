from __future__ import with_statement, nested_scopes, generators

import re
import os
import gc
import sys
import time
import threading
from functools import wraps, partial
from itertools import *
from StringIO import StringIO
from contextlib import contextmanager

# the interpreter periodically does some stuff that slows you
# down if you aren't using threads.
#sys.setcheckinterval(10000)

@contextmanager
def preserve_cwd():
    """ contenxt manager to preserve current working directory """
    cwd = os.getcwd()
    yield
    os.chdir(cwd)


def preserve_cwd_dec(f):
    """ decorator to preserve current working directory """
    @wraps(f)
    def wrap(*args, **kwargs):
        with preserve_cwd():
            return f(*args, **kwargs)
    return wrap


#______________________________________________________________________________
# Debugging utils

def dumpobj(o, double_underscores=0):
    """Prints all the object's non-callable attributes.  If double_underscores
    is false, it will skip attributes that begin with double underscores."""
    print repr(o)
    for a in [x for x in dir(o) if not callable(getattr(o, x))]:
        if not double_underscores and a.startswith("__"):
            continue
        try:
            print "  %20s: %s " % (a, getattr(o, a))
        except:
            pass
    print ""

_count = 0
def trace(func, stream=sys.stdout):
    """
    Good old fashioned Lisp-style tracing.  Example usage:
    WARNING: definitely not thread safe

    >>> def f(a, b, c=3):
    >>>     print a, b, c
    >>>     return a + b
    >>>
    >>>
    >>> f = trace(f)
    >>> f(1, 2)
    |>> f called args: [1, 2]
    1 2 3
    <<| f returned 3
    3

    TODO: print out default keywords (maybe)
    """
    name = func.func_name
    global _count
    def tracer(*args, **kw):
        global _count
        s = ('\t' * _count) + '|>> %s called with' % name
        _count += 1
        if args:
            s += ' args: %r' % list(args)
        if kw:
            s += ' kw: %r' % kw
        print >>stream, s
        ret = func(*args, **kw)
        _count -= 1
        print >>stream, ('\t' * _count) + '<<| %s returned %s' % (name, ret)
        return ret
    return tracer


def get_current_traceback_tuple():
    """Returns a semiformatted traceback of the current exception as a tuple
    in this form:
       (exceptionclass, exceptioninstance, lines_of_string_traceback_lines)"""
    import traceback
    exceptionclass, exceptioninstance, tb = sys.exc_info()
    tb_lines = traceback.format_tb(tb)
    return (exceptionclass, exceptioninstance, tb_lines)

#_________________________________________________________________________
#

@contextmanager
def ctx_redirect_io():
    """
    Usage Example:
        with ctx_redirect_io() as io_target:
            print 'how is this for io?'
        print 'redirected>', repr(io_target.getvalue())
    """
    target = StringIO()

    # Redirect IO to target.
    original_stdout = sys.stdout
    sys.stdout = target

    # provide an entry point for the procedure we are wrapping
    # as well as a reference to target
    yield target

    # Restore stdio and close the file.
    sys.stdout = original_stdout


def redirect_io(f):
    """
    Usage Example:
        @redirect_io
        def foo(x):
            print x
        foo('hello there?')
        print 'redirected>', foo.io_target.getvalue()
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        with ctx_redirect_io() as io_target:
            wrap.io_target = io_target
            return f(*args, **kwargs)
    return wrap


#______________________________________________________________________________
# Function decorators

def threaded(callback=lambda *args, **kwargs: None, daemonic=False):
    """Decorate  a function to run in its own thread and report the result
    by calling callback with it."""
    def innerDecorator(func):
        def inner(*args, **kwargs):
            target = lambda: callback(func(*args, **kwargs))
            t = threading.Thread(target=target)
            t.setDaemon(daemonic)
            t.start()
        return inner
    return innerDecorator

def garbagecollect(f):
    """ Decorate a function to invoke the garbage collecter after each
    execution. """
    @wraps(f)
    def inner(*args, **kwargs):
        result = f(*args, **kwargs)
        gc.collect()
        return result
    return inner

## TODO: add option to suppress a some user-defined list of Exceptions
def try_k_times(fn, args, k, pause=0.1):
    """ attempt to call fn up to k times with the args as arguments.
        All exceptions up to the kth will be ignored. """
    exception = None
    for i in xrange(k):
        try:
            output = fn(*args)
            break
        except Exception, e:
            exception = e
        time.sleep(pause)
    else:
        raise Exception(str(exception))
    return output

def try_k_times_decorator(k, pause=0.1):
    def wrap2(fn):
        @wraps(fn)
        def wrap(*args):
            return try_k_times(fn, args, k, pause=pause)
        return wrap
    return wrap2

# TODO:
#  * add option to pass in a reference to your own cache (maybe even a memcached client).
class memoize(object):
    """ cache a function's return value to avoid recalulation """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            if args in self.cache:
                return self.cache[args]
            else:
                self.cache[args] = value = self.func(*args)
                return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
    def __repr__(self):
        """ Return the function's docstring. """
        return self.func.__doc__


class Dispatch(threading.Thread):
    def __init__(self, f, *args, **kwargs):
        threading.Thread.__init__(self)
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
            # score exception information in the thread.
            self.error = sys.exc_info()


class TimeoutError(Exception):
    pass

def timelimit(timeout):
    """
    A decorator to limit a function to `timeout` seconds, raising TimeoutError
    if it takes longer.

        >>> import time
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
            c = Dispatch(f, *args, **kwargs)
            c.join(timeout)
            if c.isAlive():
                raise TimeoutError('took too long')
            if c.error:
                raise c.error[0], c.error[1]
            return c.result
        return _2
    return _1


def assert_throws(exc):
    def wrap1(f):
        @wraps(f)
        def wrap2(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except exc, e:
                print 'pass.'
            except Exception, e:
                print 'function raised a different Exception than required:'
                raise
            else:
                if exc is not None:
                    raise Exception('TEST-FAILED: %s did not raise required %s.' % (f.__name__, exc.__name__))
                else:
                    print 'pass.'
        return wrap2
    return wrap1


class ondemand(property):
    """A property that is loaded once from a function."""
    def __init__(self, fget, doc=None):
        property.__init__(self, fget=self.get, fdel=self.delete, doc=doc)
        self.loadfunc = fget
        import weakref
        self.values = weakref.WeakKeyDictionary()
    def get(self, obj):
        if obj not in self.values:
            self.load(obj)
        return self.values[obj]
    def load(self, obj):
        self.values[obj] = self.loadfunc(obj)
    def delete(self, obj):
        # XXX this may not be needed any more
        try:
            del self.values[obj]
        except:
            pass


if __name__ == '__main__':

    def run_tests():

        def nasty_function():
            os.chdir('..')
            os.chdir('..')

        def test_cwd_ctx_manager():
            print 'test_cwd_ctx_manager:'
            before = os.getcwd()
            with preserve_cwd():
                nasty_function()
            assert before == os.getcwd()
            print 'pass.'

        def test_preserve_cwd_dec():
            print 'test_preserve_cwd_dec:'
            @preserve_cwd_dec
            def foo():
                nasty_function()
            cwd_before = os.getcwd()
            foo()
            assert os.getcwd() == cwd_before
            print 'pass.'

        test_cwd_ctx_manager()
        test_preserve_cwd_dec()

        #---

        @assert_throws(ZeroDivisionError)
        def test_assert_throws1():
            print 'test_assert_throws1'
            0/0
        test_assert_throws1()

        @assert_throws(None)
        def test_assert_throws1():
            print 'test_assert_throws1'
            return 2 + 2
        test_assert_throws1()

        #---

        @assert_throws(TimeoutError)
        def test_timed():
            print 'test_timed'
            @timelimit(1.0)
            def sleepy_function(x):
                time.sleep(x)
            sleepy_function(3.0)

        test_timed()

        #---

        @redirect_io
        def foo(x):
            print x
        msg = 'hello there?'
        foo(msg)
        assert str(foo.io_target.getvalue().strip()) == msg

    run_tests()
