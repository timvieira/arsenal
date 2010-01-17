from __future__ import with_statement, nested_scopes, generators

import re
import os
import gc
import sys
import pdb
import time
import threading
from functools import wraps, partial
from itertools import *
from StringIO import StringIO
from contextlib import contextmanager



# TODO:
# * I see a lot of potential in this function
#   it might be a good place for code generation and other interesting things
# * borrow ideas form the "decorator" module
def decorator(d):
    """ automatically preserves the-functions-being-decorated's signature 
    
    Example:
    >>> def goo(f): return lambda *args, **kw: f(*args,**kw)
    >>> def foo(): pass
    >>> foo.__name__
    'foo'
    >>> goo(foo).__name__
    '<lambda>'
    >>> goo = decorator(goo)
    >>> goo(foo).__name__
    'foo'
    """
    @wraps(d)
    def f1(f):
        f3 = d(f)
        @wraps(f)
        def f2(*args, **kw):
            return f3(*args, **kw)
        return f2
    return f1


# the interpreter periodically does some stuff that slows you
# down if you aren't using threads.
#sys.setcheckinterval(10000)

@contextmanager
def preserve_cwd():
    """ context manager to preserve current working directory

    Usage example:
        >>> before = os.getcwd()
        >>> with preserve_cwd():
        ...     os.chdir('..')
        >>> before == os.getcwd()
        True
    """
    cwd = os.getcwd()
    yield
    os.chdir(cwd)


def preserve_cwd_dec(f):
    """ decorator to preserve current working directory

    Usage example:
        >>> before = os.getcwd()
        >>> @preserve_cwd_dec
        ... def foo():
        ...     os.chdir('..')
        >>> before == os.getcwd()
        True
    """
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

def into_debugger(f):
    """ hops into the pdb (debugger) if the decorated function dies via uncaught exception. """
    @wraps(f)
    def f1(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            pdb.post_mortem()
    return wrap

#_________________________________________________________________________
#

@contextmanager
def ctx_redirect_io():
    r"""
    Usage example:
        >>> with ctx_redirect_io() as io_target:
        ...    print 'how is this for io?'
        >>> io_target.getvalue()
        'how is this for io?\n'
        >>> print io_target.getvalue()   # doctest:+NORMALIZE_WHITESPACE
        how is this for io?
        >>>

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
    redirect all of the output to standard out to a StringIO instance,
    which can be accessed as an attribute of the function, f.io_target

    Usage Example:
        >>> @redirect_io
        ... def foo(x):
        ...    print x
        >>> foo('hello?')
        >>> print foo.io_target.getvalue()    # doctest:+NORMALIZE_WHITESPACE
        hello?
        >>>
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
    @wraps(func)
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
    @wraps(fn)
    def wrap2(fn):
        @wraps(fn)
        def wrap(*args):
            return try_k_times(fn, args, k, pause=pause)
        return wrap
    return wrap2

# TODO:
#  * add option to pass a reference to another cache (maybe memcached client)
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

import atexit
import cPickle as pickle
class memoize_persistent(object):
    """
    cache a function's return value to avoid recalulation and save the 
    cache (via pickle) at system exit so that it persists.

    WARNING: retrieves cache for functions which might not be equivalent
             if a revision is made to the code which is used to compute it.
    """
    def __init__(self, func):
        self.func = func
        self.filename = '{self.func.__name__}.cache.pkl~'.format(self=self)

        key = 0

        def save():
            if self.cache:
                pickle.dump((self.cache, key), file(self.filename,'wb'))
                print 'atexit: saved persistent cache for {self.func.__name__} to file "{self.filename}"'.format(self=self)
        atexit.register(save)

        loaded_key = None
        try:
            (cache, loaded_key) = pickle.load(file(self.filename,'r'))
        except IOError:
            pass
        finally:
            if key == loaded_key:
                self.cache = cache
                print 'loaded cache for {self.func.__name__}'.format(self=self)
            else:
                self.cache = {}
                print 'failed to load cache for {self.func.__name__}'.format(self=self)

    def __call__(self, *args):
        try:
            if args in self.cache:
                return self.cache[args]
            else:
                self.cache[args] = value = self.func(*args)
                return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            raise TypeError('uncachable instance passed to memoized function.')
            # Better to not cache than to blow up entirely?
            #return self.func(*args)


def print_elapsed_time():
    begin = time.clock()
    started = time.localtime()
    def handler():
        secs = time.clock() - begin
        mins, secs = divmod(secs, 60)
        hrs, mins = divmod(mins, 60)       
        print
        print '======================================================================'
        print 'Started on', time.strftime("%B %d, %Y at %I:%M:%S %p", started)
        print 'Finished on', time.strftime("%B %d, %Y at %I:%M:%S %p", time.localtime())
        print 'Total time:', '%02d:%02d:%02d' % (hrs, mins, secs)
        print
    atexit.register(handler)

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


## XXX: This is more of a job for a context manager...
def assert_throws(exc):
    """
    >>> @assert_throws(ZeroDivisionError)
    ... def foo():
    ...     1 + 1   # should not raise ZeroDivisionError
    ...
    >>> foo()
    Traceback (most recent call last):
        ...
    Exception: TEST: foo did not raise required ZeroDivisionError.
    """
    def wrap1(f):
        @wraps(f)
        def wrap2(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except exc, e:
                pass
            except Exception, e:
                print 'function raised a different Exception than required:'
                raise
            else:
                if exc is not None:
                    raise Exception('TEST: %s did not raise required %s.' \
                                        % (f.__name__, exc.__name__))
                else:
                    pass
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


# borrowed from IPython
def debug_expr(expr, msg=''):
    """
    Print the value of an expression from the caller's frame.

    Takes an expression, evaluates it in the caller's frame and prints both
    the given expression and the resulting value (as well as a debug mark
    indicating the name of the calling function.  The input must be of a form
    suitable for eval().
    """
    cf = sys._getframe(1)
    val = eval(expr, cf.f_globals, cf.f_locals)
    print '[DEBUG:%s] %s%s -> %r' % (cf.f_code.co_name, msg, expr, val)


import inspect
def debugx(obj):
    """
    I often write debugging print statements which look like
      >>> somevar = 'somevalue'
      >>> print 'somevar:', somevar
      somevar: somevalue

    What this function attempts to do is provide a shortcut
      >>> debugx(somevar)
      somevar: somevalue

    Warning: this should only be used for debugging because ir relies on 
    introspection, which can be really slow and sometimes even buggy.
    """

    cf = sys._getframe(1)
    ctx_lines = inspect.getframeinfo(cf).code_context
    code = ''.join(map(str.strip, ctx_lines))

    code = re.sub('debugx\((.*)\)', r'\1', code)
    print code + ':', obj
    

def marquee(txt='',width=78,mark='*'):
    """
    Return the input string centered in a 'marquee'.

    >>> marquee('hello', width=50)
    '********************* hello *********************'

    """
    if not txt:
        return (mark*width)[:width]
    nmark = (width-len(txt)-2)/len(mark)/2
    if nmark < 0: nmark =0
    marks = mark*nmark
    return '%s %s %s' % (marks,txt,marks)


if __name__ == '__main__':

    def run_tests():

        def test_cwd_ctx_manager():
            print 'test_cwd_ctx_manager:'
            before = os.getcwd()
            with preserve_cwd():
                os.chdir('..')
                os.chdir('..')
            assert before == os.getcwd()
            print 'pass.'

        def test_preserve_cwd_dec():
            print 'test_preserve_cwd_dec:'
            @preserve_cwd_dec
            def foo():
                os.chdir('..')
                os.chdir('..')
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

if __name__ == '__main__':
    run_tests()
    import doctest; doctest.testmod()

    x = 15
    debug_expr('x')

    debugx(x)
    debugx(x**2 + 2*x + 3)
    f = lambda x: x**2
    debugx(f(x))
