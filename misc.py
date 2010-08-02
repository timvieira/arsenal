import re, os, sys, time
import datetime
import gc
import inspect
import pdb
import atexit
import weakref
import threading
import warnings
import BaseHTTPServer
import webbrowser
import subprocess, tempfile
from functools import wraps
from StringIO import StringIO
from contextlib import contextmanager

#def trace(f):
#    def wrap(*args, **kw):
#        print 'calling function: {f} with args: {args} kwargs: {kw}'.format(f=f, args=args, kw=kw)
#        y = f(*args, **kw)
#        print ' ->', y
#        return y
#    return wrap

## I'm not sure about this function yet..
## def deep_import(name):
##     """
##     A version of __import__ that works as expected when using the form 
##     'module.name' (returns the object corresponding to 'name', instead of 
##     'module').
##     """
##     mod = __import__(name)
##     components = name.split('.')
##     for comp in components[1:]:
##         mod = getattr(mod, comp)
##     return mod

@contextmanager
def print_time(msg="%.4f seconds"):
    b4 = time.time()
    yield
    print msg % (time.time() - b4)


def deprecated(use_instead=None):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    assert not use_instead or isinstance(use_instead, str)

    def wrapped(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            message = "Call to deprecated function %s." % func.__name__
            if use_instead:
                message += " Use %s instead." % use_instead
            warnings.warn(message, category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return new_func

    return wrapped


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


def use_pager(s, pager='less'):
    """Use the pager passed in and send string s through it."""
    p = subprocess.Popen(pager, stdin=subprocess.PIPE)
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
        print 'called completer...'

        # keep a completer class, make sure that it uses the current local scope
        if not hasattr(self, 'completer'):
            self.completer = rlcompleter.Completer(self.curframe.f_locals)
        else:
            self.completer.namespace = self.curframe.f_locals
        return self.completer.complete(text, state)

    # replace the Pdb class's complete method with ours
    Pdb = sys._getframe(2).f_globals['Pdb']
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


'''
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
'''

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
        >>> foo()
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
        self._cwd = None

    def __enter__(self):
        self._cwd = os.getcwd()

    def __exit__(self, *args):
        os.chdir(self._cwd)

    def __call__(self, *args, **kwargs):
        with self:
            return self.f(*args, **kwargs)


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
    for _ in xrange(k):
        try:
            output = fn(*args)
            break
        except Exception as e:
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
    AssertionError: did not raise required ZeroDivisionError. Got None instead.
    """
    def wrap(f):
        @wraps(f)
        def wrap2(*args,**kw):
            with assert_throws_ctx(exc):
                return f(*args,**kw)
        return wrap2
    return wrap

@contextmanager
def assert_throws_ctx(*exc):
    """
    Contextmanager for asserting that a certain exception or no exception will
    arise with it's context.

    >>> with assert_throws_ctx(ZeroDivisionError):
    ...     1/0

    >>> with assert_throws_ctx(None):
    ...     pass

    >>> with assert_throws_ctx(None, ZeroDivisionError):
    ...     pass

    >>> with assert_throws_ctx(ZeroDivisionError):
    ...     pass
    Traceback (most recent call last):
        ...
    AssertionError: did not raise required ZeroDivisionError. Got None instead.

    >>> with assert_throws_ctx(AssertionError, ZeroDivisionError):
    ...     pass
    Traceback (most recent call last):
        ...
    AssertionError: did not raise required AssertionError or ZeroDivisionError. Got None instead.

    """

    passed = False
    got = None
    try:
        yield
    except exc:
        passed = True
    except Exception as e:
        got = e
    else:
        # since None isn't realy an exception, we have to special case it.
        if None in exc:
            passed = True
    finally:
        if not passed:
            msg = ' or '.join(e.__name__ if e is not None else 'None' for e in exc)
            raise AssertionError('did not raise required %s. Got %s instead.' % (msg, got))


#______________________________________________________________________________
# Debugging utils

def enable_debug_hook():
    def debug_hook(*args):
        sys.__excepthook__(*args)
        pdb.pm()
    sys.excepthook = debug_hook

def dumpobj(o, callables=0, dbl_under=0):
    print repr(o)
    print 'instance of:', type(o).__name__
    for a in dir(o):
        if not callables and callable(getattr(o, a)):
            continue
        if not dbl_under and a.startswith('__'):
            continue
        try:
            print '  %20s: %s ' % (a, type(getattr(o,a)).__name__)
        except:
            pass
    print

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

#_______________________________________________________________________________
#

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
        try:
            del self.values[obj]
        except:
            pass


class cached_property(object):
    """
    Lazy-loading read/write property descriptor.
    Value is stored locally in descriptor object. If value is not set when
    accessed, value is computed using given function. Value can be cleared
    by calling 'del'.
    """
    def __init__(self, func):
        self._func = func
        self._values = {}
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, obj_class):
        if obj is None:
            return obj
        if obj not in self._values or self._values[obj] is None:
            self._values[obj] = self._func(obj)
        return self._values[obj]

    def __set__(self, obj, value):
        self._values[obj] = value

    def __delete__(self, obj):
        if self.__name__ in obj.__dict__:
            del obj.__dict__[self.__name__]
        self._values[obj] = None

#_______________________________________________________________________________
#

def nthstr(n):
    """
    Formats an ordinal.
    Doesn't handle negative numbers.

    >>> nthstr(1)
    '1st'
    >>> nthstr(0)
    '0th'
    >>> [nthstr(x) for x in [2, 3, 4, 5, 10, 11, 12, 13, 14, 15]]
    ['2nd', '3rd', '4th', '5th', '10th', '11th', '12th', '13th', '14th', '15th']
    >>> [nthstr(x) for x in [91, 92, 93, 94, 99, 100, 101, 102]]
    ['91st', '92nd', '93rd', '94th', '99th', '100th', '101st', '102nd']
    >>> [nthstr(x) for x in [111, 112, 113, 114, 115]]
    ['111th', '112th', '113th', '114th', '115th']
    """    
    assert n >= 0
    if n % 100 in [11, 12, 13]: return '%sth' % n
    return {1: '%sst', 2: '%snd', 3: '%srd'}.get(n % 10, '%sth') % n


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



def datestr(then, now=None):
    """
    Converts a (UTC) datetime object to a nice string representation.
    
        >>> from datetime import datetime, timedelta
        >>> d = datetime(1970, 5, 1)
        >>> datestr(d, now=d)
        '0 microseconds ago'
        >>> for t, v in {
        ...   timedelta(microseconds=1): '1 microsecond ago',
        ...   timedelta(microseconds=2): '2 microseconds ago',
        ...   -timedelta(microseconds=1): '1 microsecond from now',
        ...   -timedelta(microseconds=2): '2 microseconds from now',
        ...   timedelta(microseconds=2000): '2 milliseconds ago',
        ...   timedelta(seconds=2): '2 seconds ago',
        ...   timedelta(seconds=2*60): '2 minutes ago',
        ...   timedelta(seconds=2*60*60): '2 hours ago',
        ...   timedelta(days=2): '2 days ago',
        ... }.iteritems():
        ...     assert datestr(d, now=d+t) == v
        >>> datestr(datetime(1970, 1, 1), now=d)
        'January  1'
        >>> datestr(datetime(1969, 1, 1), now=d)
        'January  1, 1969'
        >>> datestr(datetime(1970, 6, 1), now=d)
        'June  1, 1970'
        >>> datestr(None)
        ''
    """
    def agohence(n, what, divisor=None):
        if divisor: n = n // divisor

        out = str(abs(n)) + ' ' + what       # '2 day'
        if abs(n) != 1: out += 's'           # '2 days'
        out += ' '                           # '2 days '
        if n < 0:
            out += 'from now'
        else:
            out += 'ago'
        return out                           # '2 days ago'

    oneday = 24 * 60 * 60

    if not then: return ""
    if not now: now = datetime.datetime.utcnow()
    if type(now).__name__ == "DateTime":
        now = datetime.datetime.fromtimestamp(now)
    if type(then).__name__ == "DateTime":
        then = datetime.datetime.fromtimestamp(then)
    elif type(then).__name__ == "date":
        then = datetime.datetime(then.year, then.month, then.day)

    delta = now - then
    deltaseconds = int(delta.days * oneday + delta.seconds + delta.microseconds * 1e-06)
    deltadays = abs(deltaseconds) // oneday
    if deltaseconds < 0: deltadays *= -1 # fix for oddity of floor

    if deltadays:
        if abs(deltadays) < 4:
            return agohence(deltadays, 'day')

        out = then.strftime('%B %e') # e.g. 'June 13'
        if then.year != now.year or deltadays < 0:
            out += ', %s' % then.year
        return out

    if int(deltaseconds):
        if abs(deltaseconds) > (60 * 60):
            return agohence(deltaseconds, 'hour', 60 * 60)
        elif abs(deltaseconds) > 60:
            return agohence(deltaseconds, 'minute', 60)
        else:
            return agohence(deltaseconds, 'second')

    deltamicroseconds = delta.microseconds
    if delta.days: deltamicroseconds = int(delta.microseconds - 1e6) # datetime oddity
    if abs(deltamicroseconds) > 1000:
        return agohence(deltamicroseconds, 'millisecond', 1000)

    return agohence(deltamicroseconds, 'microsecond')


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
    "register an exit hook which prints the start, finish, and elapsed times of a script."
    begin = time.clock()
    started = time.localtime()
    def hook():
        secs = time.clock() - begin
        mins, secs = divmod(secs, 60)
        hrs, mins = divmod(mins, 60)
        print
        print '======================================================================'
        print 'Started on', time.strftime("%B %d, %Y at %I:%M:%S %p", started)
        print 'Finished on', time.strftime("%B %d, %Y at %I:%M:%S %p", time.localtime())
        print 'Total time: %02d:%02d:%02d' % (hrs, mins, secs)
        print
    atexit.register(hook)


if __name__ == '__main__':

    import doctest

    def run_tests():

        def test_preserve_cwd():
            before = os.getcwd()
            with preserve_cwd():
                os.chdir('..')
                os.chdir('..')
            assert before == os.getcwd()

            @preserve_cwd
            def foo():
                os.chdir('..')
                os.chdir('..')
            cwd_before = os.getcwd()
            foo()
            assert os.getcwd() == cwd_before

        test_preserve_cwd()


        @assert_throws(ZeroDivisionError)
        def test_assert_throws1():
            1/0
        test_assert_throws1()

        @assert_throws(None)
        def test_assert_throws1():
            return 2 + 2
        test_assert_throws1()


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

        def test_redirect_io():
            @redirect_io
            def foo(x):
                print x
            msg = 'hello there?'
            foo(msg)
            assert str(foo.io_target.getvalue().strip()) == msg

        test_redirect_io()

        def test_debug_expressions():
            x = 15
            debug_expr('x')
    
            debugx(x)
            debugx(x**2 + 2*x + 3)
            f = lambda x: x**2
            debugx(f(x))
        test_debug_expressions()

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


        def test_lazy():
            import pickle

            global Foo
            # class Foo needs to be in __main__ scope for pickling to work.
            class Foo(object):
                def __init__(self, x):
                    self.x = x
                @ondemand
                def my_ondemand(self):
                    print '\033[31mcomputing ondemand property\033[0m'
                    return 'ON DEMAND'
                @cached_property
                def my_cached(self):
                    print '\033[31mcomputing cached property\033[0m'
                    return 'CACHED PROPERTY'

            foo = Foo('XXX')
            debugx(foo.my_ondemand)
            debugx(foo.my_cached)
            print '....'
            debugx(foo.my_ondemand)
            debugx(foo.my_cached)

            print marquee('begin pickle')
            foo_pkl = pickle.dumps(foo)
            foo2 = pickle.loads(foo_pkl)
            print foo_pkl
            print marquee('end pickle')

            debugx(foo2.my_ondemand)
            debugx(foo2.my_cached)
            print '....'
            debugx(foo2.my_ondemand)
            debugx(foo2.my_cached)

        test_lazy()

        class FooBurger(object):
            x = 10
            def __init__(self, y):
                self.y = y
            def span(self):
                print 'spam:', y

        dumpobj(FooBurger('WHY'))
        dumpobj(FooBurger('WHY'), 1, 0)
        dumpobj(FooBurger('WHY'), 0, 1)


    run_tests()

    doctest.testmod()
