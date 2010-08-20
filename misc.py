import re, os, sys, time
import gc
import inspect
import pdb
import atexit
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

@deprecated(use_instead='timeit')
def print_time(msg="%.4f seconds"):
    return timeit(msg)

@contextmanager
def timeit(msg="%.4f seconds"):
    """Context Manager which prints the time it took to run code block."""
    b4 = time.time()
    yield
    print msg % (time.time() - b4)


def find_files(d, filterfn=lambda x: True, relpath=True):
    """
    Recursively walks directory `d` yielding files which satisfy `filterfn`.
    Set option `relpath` to False to output absolute paths.
    """
    for dirpath, _, filenames in os.walk(d):
        for f in filenames:
            if relpath:
                f = os.path.join(dirpath, f)   # TIM: should I call abspath here?
            if filterfn(f):
                yield f


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
    def innerDecorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            target = lambda: callback(func(*args, **kwargs))
            t = threading.Thread(target=target)
            t.setDaemon(daemonic)
            t.start()
        return inner
    return innerDecorator

def dump_garbage():
    """
    Show us what's in the garbage!

    Make a leak:
      l = []
      l.append(l)
      del l

    Show the dirt:
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





#_______________________________________________________________________________
#

def try_k_times(fn, args, k, pause=0.1, suppress=(Exception,)):
    """ attempt to call fn up to k times with the args as arguments.
        All exceptions up to the kth will be ignored. """
    for i in xrange(k):
        try:
            return fn(*args)
        except suppress:
            if i == k - 1:  # the last iteration
                raise
        time.sleep(pause)

def try_k_times_decorator(k, pause=0.1):
    def wrap2(fn):
        @wraps(fn)
        def wrap(*args):
            return try_k_times(fn, args, k, pause=pause)
        return wrap
    return wrap2

#_______________________________________________________________________________
#



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
    from assertutils import assert_throws_ctx

    def run_tests():

        def test_try_k_times():

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
            assert try_k_times(f, (1,2,3), 5)
            assert f.tries == 5

            with assert_throws_ctx(NotCalledEnough):
                f = TroublsomeFunction()
                print try_k_times(f, (10,), 2)

        test_try_k_times()


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
            def raises_errors(): return 1/0
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

        print
        print 'testing dumpobj...'
        class FooBurger(object):
            x = 10
            def __init__(self, y):
                self.y = y
            def span(self):
                print 'spam:', self.y

        dumpobj(FooBurger('WHY'))
        dumpobj(FooBurger('WHY'), 1, 0)
        dumpobj(FooBurger('WHY'), 0, 1)


    run_tests()

    doctest.testmod()

