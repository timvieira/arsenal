# stdlib
import re, os, sys, time
import gc
import atexit
import warnings
import BaseHTTPServer
import webbrowser
import subprocess, tempfile
from functools import wraps
from StringIO import StringIO
from contextlib import contextmanager
from threading import Thread

# python-extras imports
from terminal import colors

# this which used to be in this module
from fsutils import preserve_cwd
from humanreadable import marquee

def attn(msg):
    """ Display a dialog which is sure to get my attention. """
    import gtk
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("delete_event", lambda *x: False)
    window.connect("destroy", lambda *x: gtk.main_quit())
    window.set_border_width(10)
    button = gtk.Button(msg)
    button.connect_object("clicked", gtk.Widget.destroy, window)
    window.add(button)
    button.show()
    window.show()
    window.fullscreen()
    gtk.main()


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

'''
import difflib
def showdiff(old, new):
    d = difflib.Differ()
    lines = d.compare(old.lines(),new.lines())
    realdiff = False
    for l in lines:
        print l,
        if not realdiff and not l[0].isspace():
            realdiff = True
    return realdiff
'''

def piped():
    """Returns piped input via stdin, else False"""
    with sys.stdin as stdin:
        return stdin.read() if not stdin.isatty() else None

def highlighter(p, flags=0):
    pattern = re.compile('%s' % p, flags)
    return lambda x: pattern.sub(colors.bold % colors.yellow % colors.bg_red % r'\1', x)

def deprecated(use_instead=None):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

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


@contextmanager
def timeit(msg="%.4f seconds", header=None):
    """Context Manager which prints the time it took to run code block."""
    if header is not None:
        print header
    b4 = time.time()
    yield
    print msg % (time.time() - b4)

timesection = lambda x: timeit(header='%s...' % x,
                               msg=' -> %s took %%.2f seconds' % x)


def browser(html):
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


def pager(s, pager='less'):
    """Use the pager passed in and send string s through it."""
    subprocess.Popen(pager, stdin=subprocess.PIPE).communicate(s)


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
            t = Thread(target=target)
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


#_______________________________________________________________________________
#

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


        def test_redirect_io():
            @redirect_io
            def foo(x):
                print x
            msg = 'hello there?'
            foo(msg)
            assert str(foo.io_target.getvalue().strip()) == msg

        test_redirect_io()


        from debug.utils import dumpobj

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
