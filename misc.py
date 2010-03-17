from __future__ import with_statement, nested_scopes, generators

import re, os, gc, sys, pdb, time, atexit, inspect, weakref, threading, warnings

import BaseHTTPServer
import webbrowser

import cPickle as pickle
import subprocess, tempfile

from functools import wraps, partial
from StringIO import StringIO
from contextlib import contextmanager


#def trace(f):
#    def wrap(*args, **kw):
#        print 'calling function: {f} with args: {args} kwargs: {kw}'.format(f=f, args=args, kw=kw)
#        y = f(*args, **kw)
#        print ' ->', y
#        return y
#    return wrap


def enable_debug_hook():
    def debug_hook(*args):
        sys.__excepthook__(*args)
        pdb.pm()
    sys.excepthook = debug_hook

from bsddb.db import DBPageNotFoundError
import shelve
class ShelfBasedCache(object):
    """ cache a function's return value to avoid recalulation and save cache in a shelve. """
    def __init__(self, func, key):
        self.func = func
        self.filename = '{self.func.__name__}.shelf~'.format(self=self)
        self.cache = shelve.open(self.filename) #, writeback=True)
        self.key = key
        self.__name__ = 'ShelfBasedCache(%s)' % func.__name__
    def __call__(self, *args):
        p_args = self.key(args)

        if self.cache.has_key(p_args):
            return self.cache[p_args]
        else:
            self.cache[p_args] = value = self.func(*args)
            self.cache.sync()
            return value
    def __del__(self):
        self.cache.close()

def persistent_cache(key):
    def wrap(f):
        return ShelfBasedCache(f, key)
    return wrap


'''
@contextmanager
def atomic():
    """ hack for executing blocks of code atomically. """
    try:
        sys.setcheckinterval(sys.maxint)
        # statements in this block are
        # assured to run atomically
        yield
    finally:
        sys.setcheckinterval(100)
'''    

# the interpreter periodically does some stuff that slows you
# down if you aren't using threads.
#sys.setcheckinterval(10000)

def LoadInBrowser(html):
    """Display html in the default web browser without creating a temp file.

    Instantiates a trivial http server and calls webbrowser.open with a URL
    to retrieve html from that server.
    """

    class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):
            bufferSize = 1024*1024
            for i in xrange(0, len(html), bufferSize):
                self.wfile.write(html[i:i+bufferSize])

    server = BaseHTTPServer.HTTPServer(('127.0.0.1', 0), RequestHandler)
    webbrowser.open('http://127.0.0.1:%s' % server.server_port)
    server.handle_request()


def use_pager(s, pager=None):
    """Use the pager passed in and send string s through it."""
    pager = os.environ.get('PAGER', 'less')  # default pager is less
    p = subprocess.Popen([pager], stdin=subprocess.PIPE)
    p.communicate(s)


def edit_with_editor(s=None):
    """
    Open os.environ['EDITOR'] and load in text s.

    Returns the text typed in the editor, after running strip().
    """
    # This is the first time I've used with!
    with tempfile.NamedTemporaryFile() as t:
        if s:
            t.write(str(s))
            t.seek(0)
        subprocess.call([os.environ.get('EDITOR', 'nano'), t.name])
        return t.read().strip()

'''
import os
import sys
import rlcompleter
#import readline
#readline.parse_and_bind("tab: complete")

def pdb_completer():
    # refresh the terminal
    #os.system("stty sane")

    def complete(self, text, state):
        """return the next possible completion for text, using the current
           frame's local namespace

           This is called successively with state == 0, 1, 2, ... until it
           returns None.  The completion should begin with 'text'.
        """

        print 'called complter...'

        # keep a completer class, make sure that it uses the current local scope
        if not hasattr(self, 'completer'):
            self.completer = rlcompleter.Completer(self.curframe.f_locals)
        else:
            self.completer.namespace = self.curframe.f_locals
        return self.completer.complete(text, state)


    # replace the Pdb class's complete method with ours
    Pdb = sys._getframe(2).f_globals['Pdb']
    Pdb.complete = complete.__get__(Pdb)


    Pdb.complete = complete.__get__(Pdb)

    # set use_rawinput to 1 as tab completion relies on rawinput being used
    self = sys._getframe(2).f_locals['self']
    self.use_rawinput = 1
'''


## class defaultdict2(dict):
##     """
##     Example of the __missing__ method of the dictionary class
##     """
##     def __init__(self, factory, factArgs=(), dictArgs=()):
##         dict.__init__(self, *dictArgs)
##         self.factory = factory
##         self.factArgs = factArgs
##     def __missing__(self, key):
##         self[key] = self.factory(*self.factArgs)


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit("Call to deprecated function %s." % func.__name__,
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1)
        return func(*args, **kwargs)

    return new_func


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


## def preserve_cwd_dec(f):
##     """ decorator to preserve current working directory
## 
##     Usage example:
##         >>> before = os.getcwd()
##         >>> @preserve_cwd_dec
##         ... def foo():
##         ...     os.chdir('..')
##         >>> before == os.getcwd()
##         True
##     """
##     @wraps(f)
##     def wrap(*args, **kwargs):
##         with preserve_cwd():
##             return f(*args, **kwargs)
##     return wrap
## 
## 
## @contextmanager
## def preserve_cwd():
##     """ context manager to preserve current working directory
## 
##     Usage example:
##     """
##     cwd = os.getcwd()
##     yield
##     os.chdir(cwd)

class preserve_cwd(object):
    """
    context-manager which doubles as a decorator that preserve current 
    working directory.

    Usage example:

    As a decorator:
        >>> before = os.getcwd()
        >>> @preserve_cwd
        ... def foo():
        ...     os.chdir('..')
        >>> before == os.getcwd()
        True

    As a context-manager:
        >>> before = os.getcwd()
        >>> with preserve_cwd():
        ...     os.chdir('..')
        >>> before == os.getcwd()
        True

    """

    def __init__(self, f=None):
        self.f = f

    def __enter__(self):
        self._cwd = os.getcwd()

    def __exit__(self, *args):
        os.chdir(self._cwd)        

    def __call__(self, *args, **kwargs):
        with self:
            return self.f(*args, **kwargs)

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

def dump_garbage():
    """
    show us what's the garbage about

      # make a leak
      l = []
      l.append(l)
      del l

      # show the dirt ;-)
      dump_garbage()

    """
    import gc
    gc.enable()
    gc.set_debug(gc.DEBUG_LEAK)

    # force collection
    print "GARBAGE:"
    gc.collect()

    print "\nGARBAGE OBJECTS:"
    for x in gc.garbage:
        s = str(x)
        if len(s) > 80:
            s = s[:80] + '.........'
        print type(x),"\n    ", s


def garbagecollect(f):
    """ Decorate a function to invoke the garbage collecter after each execution. """
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

## TODO: automatically make a back-up of the pickle
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
        self.dirty = False
        self.key = 0
        self.cache = {}
        self.loaded = False
        atexit.register(self.save)

    def save(self):
        if self.cache and self.dirty:
            pickle.dump((self.cache, self.key), file(self.filename,'wb'))
            print '[ATEXIT] saved persistent cache for {self.func.__name__} to file "{self.filename}"'.format(self=self)
        else:
            print "[ATEXIT] found nothing to save in {self.func.__name__}'s cache.".format(self=self)

    def load(self):
        self.loaded = True
        loaded_key = None
        try:
            (cache, loaded_key) = pickle.load(file(self.filename,'r'))
        except IOError:
            pass
        finally:
            if self.key == loaded_key:
                self.cache = cache
                print 'loaded cache for {self.func.__name__}'.format(self=self)
            else:
                self.cache = {}
                print 'failed to load cache for {self.func.__name__}'.format(self=self)

    def __call__(self, *args):
        # wait until you call the function to un-pickle
        if not self.loaded:
            self.load()

        try:
            if args in self.cache:
                return self.cache[args]
            else:
                self.dirty = True
                self.cache[args] = value = self.func(*args)
                return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            raise TypeError('uncachable instance passed to memoized function.')


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
            c = Dispatch(f, *args, **kwargs)
            c.join(timeout)
            if c.isAlive():
                raise TimeoutError('took too long')
            if c.error:
                raise c.error[1]
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
                print 'raised a different Exception than required:'
                raise
            else:
                if exc is not None:
                    raise Exception('TEST: %s did not raise required %s.' \
                                        % (f.__name__, exc.__name__))
                else:
                    pass
        return wrap2
    return wrap1

@contextmanager
def assert_throws_ctx(*exc):
    """
    Contextmanager for asserting that a certain exception or no exception will
    arise with it's context.

    >>> with assert_throws_ctx(ZeroDivisionError):
    ...     1 / 0

    >>> with assert_throws_ctx(None):
    ...     pass

    >>> with assert_throws_ctx(ZeroDivisionError):
    ...     pass
    Traceback (most recent call last):
        ...
    Exception: did not raise required ZeroDivisionError. got None instead.

    >>> with assert_throws_ctx(AssertionError, ZeroDivisionError):
    ...     pass
    Traceback (most recent call last):
        ...
    Exception: did not raise required AssertionError or ZeroDivisionError. got None instead.

    >>> with assert_throws_ctx(None, ZeroDivisionError):
    ...     pass

    """

    passed = False
    got = None
    try:
        yield
    except exc:
        passed = True
    except Exception, e:
        got = e
    else:
        # since None isn't realy an exception, we have to special case it.
        if None in exc:
            passed = True
    finally:
        if not passed:
            msg = ' or '.join(e.__name__ if e is not None else 'None' for e in exc)
            raise Exception('did not raise required %s. got %s instead.' % (msg, got))


class ondemand(property):
    """A property that is loaded once from a function."""
    def __init__(self, fget, doc=None):
        property.__init__(self, fget=self.get, fdel=self.delete, doc=doc)
        self.loadfunc = fget
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





def htime(s):
    """htime(x) -> (days, hours, min, seconds)"""
    m, s = divmod(s, 60)
    h, m = divmod(min, 60)
    d, h = divmod(h, 24)
    return int(d), int(h), int(m), s

def sec2prettytime(diff, show_seconds=True):
    """Given a number of seconds, returns a string attempting to represent
    it as shortly as possible.

    >>> sec2prettytime(100000)
    '1d3h46m40s'
    """
    diff = int(diff)
    days, diff = divmod(diff, 86400)
    hours, diff = divmod(diff, 3600)
    minutes, seconds = divmod(diff, 60)
    x = []
    if days:
        x.append('%sd' % days)
    if hours:
        x.append('%sh' % hours)
    if minutes:
        x.append('%sm' % minutes)
    if show_seconds and seconds:
        x.append('%ss' % seconds)
    if not x:
        if show_seconds:
            x = ['%ss' % seconds]
        else:
            x = ['0m']
    return ''.join(x)

def marquee(txt='', width=78, mark='*'):
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
    return '%s %s %s' % (marks, txt, marks)


# TODO: use htime and marquee
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
        print 'Total time: %02d:%02d:%02d' % (hrs, mins, secs)
        print
    atexit.register(handler)


if __name__ == '__main__':

    import doctest

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
            @preserve_cwd
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

        def test_timed():
            print 'test_timed'

            @timelimit(1.0)
            def sleepy_function(x): time.sleep(x)

            with assert_throws_ctx(TimeoutError):
                sleepy_function(3.0)
            print 'sleepy_function(3.0): pass'

            sleepy_function(0.2)
            print 'sleepy_function(0.2): pass'

            @timelimit(1)
            def raises_errors(): 1/0
            with assert_throws_ctx(ZeroDivisionError):
                raises_errors()
            print 'raises_errors(): pass'

        test_timed()

        #---

        @redirect_io
        def foo(x):
            print x
        msg = 'hello there?'
        foo(msg)
        assert str(foo.io_target.getvalue().strip()) == msg


        x = 15
        debug_expr('x')

        debugx(x)
        debugx(x**2 + 2*x + 3)
        f = lambda x: x**2
        debugx(f(x))


        print '-----------------------------------------------'
        doctest.run_docstring_examples("""
        >>> sec2prettytime(1)
        '1s'
        >>> sec2prettytime(10)
        '10s'
        >>> sec2prettytime(100)
        '1m40s'
        >>> sec2prettytime(60)
        '1m'
        >>> sec2prettytime(1000)
        '16m40s'
        >>> sec2prettytime(10000)
        '2h46m40s'
        """, globals(), verbose=0)


    run_tests()
    doctest.testmod(verbose=0)
