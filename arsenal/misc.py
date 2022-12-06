import re, os, sys, traceback, warnings, webbrowser
import subprocess, tempfile, http.server
from functools import wraps
from io import StringIO
from contextlib import contextmanager
from arsenal import colors

# TODO: stdio/stderr redirection is available in contextlib; so is exception
# suppression and even the context decorator.


def open_diff(a, b, cmd='meld'):
    "View diff of string representations in dedicated diff program."
    print(a, file=open('/tmp/a', 'w', encoding='utf-8'))
    print(b, file=open('/tmp/b', 'w', encoding='utf-8'))
    os.system('%s /tmp/a /tmp/b' % cmd)


def deprecated(use_instead=None, msg=None):
    """
    This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """
    def wrapped(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            m = f'Call to deprecated function `{func.__name__}`.'
            if msg:
                m += f'\n{msg}'
            if use_instead:
                m += f"\nUse `{use_instead}` instead."
            warnings.warn(m, stacklevel=2)
            return func(*args, **kwargs)
        return new_func

    return wrapped


class ddict(dict):
    """
    Variation on collections.defaultdict which allows default value callback to
    inspect missing key.
    """
    def __init__(self, f):
        self.f = f
        super(ddict, self).__init__()

    def __missing__(self, key):
        self[key] = c = self.f(key)
        return c


@contextmanager
def ignore_error(color='red'):
    try:
        yield
    except:
        etype, evalue, tb = sys.exc_info()
        tb = '\n'.join(traceback.format_exception(etype, evalue, tb))

        if color is not None:
            color = getattr(colors, color)
        else:
            color = '%s'

        print(color % '*'*80)
        print(color % tb)
        print(color % '*'*80)


#@deprecated
#class logger(object):
#
#    def __init__(self, filename, clean=True, quiet=False):
#        if clean:
#            os.system('rm -f ' + filename)
#        self.f = file(filename, 'wb')
#        self.quiet = quiet
#
#    def write(self, x):
#        self.f.write(x)
#        if not self.quiet:
#            sys.__stdout__.write(x)
#
#    @staticmethod
#    def start(*args, **kw):
#        """ redirect stdout and stderr to logger """
#        log = logger(*args, **kw)
#        sys.stderr = sys.stdout = log
#        return log


def force(g):
    """ force evaluation of generator `g`. """
    @wraps(g)
    def wrap(*args, **kw):
        return list(g(*args, **kw))
    return wrap


#def attn(msg):
#    """ Display a dialog which is sure to get my attention. """
#    import gtk
#    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#    window.connect("delete_event", lambda *x: False)
#    window.connect("destroy", lambda *x: gtk.main_quit())
#    window.set_border_width(10)
#    button = gtk.Button(msg)
#    button.connect_object("clicked", gtk.Widget.destroy, window)
#    window.add(button)
#    button.show()
#    window.show()
#    window.fullscreen()
#    gtk.main()


## # borrowed from whoosh
## def find_object(name, blacklist=None, whitelist=None):
##     """Imports and returns an object given a fully qualified name.
##
##     >>> find_object("whoosh.analysis.StopFilter")
##     <class 'whoosh.analysis.StopFilter'>
##     """
##
##     if blacklist:
##         for pre in blacklist:
##             if name.startswith(pre):
##                 raise TypeError("%r: can't instantiate names starting with %r" % (name, pre))
##     if whitelist:
##         passes = False
##         for pre in whitelist:
##             if name.startswith(pre):
##                 passes = True
##                 break
##         if not passes:
##             raise TypeError("Can't instantiate %r" % name)
##
##     lastdot = name.rfind(".")
##
##     assert lastdot > -1, "Name %r must be fully qualified" % name
##     modname = name[:lastdot]
##     clsname = name[lastdot + 1:]
##
##     mod = __import__(modname, fromlist=[clsname])
##     cls = getattr(mod, clsname)
##     return cls


def piped():
    """ Returns piped input via stdin, else None. """
    return sys.stdin if not sys.stdin.isatty() else None


def highlighter(p, flags=0):
    pattern = re.compile('%s' % p, flags)
    return lambda x: pattern.sub(colors.bold % colors.yellow % colors.bg_red % r'\1', x)


def browser(html):
    """
    Display html in the default web browser without creating a temp file.

    Instantiates a trivial http server and calls webbrowser.open with a URL
    to retrieve html from that server.
    """

    class RequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            bufferSize = 1024*1024
            for i in range(0, len(html), bufferSize):
                self.wfile.write(html[i:i+bufferSize])

    server = http.server.HTTPServer(('127.0.0.1', 0), RequestHandler)
    webbrowser.open('http://127.0.0.1:%s' % server.server_port)
    server.handle_request()


def pager(s, cmd='less'):
    """Use the pager passed in and send string s through it."""
    subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate(s)


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

editor = edit_with_editor

#_________________________________________________________________________
#

# TODO: use a contextdecorator
@contextmanager
def ctx_redirect_io(f=None):
    r"""
    Usage example:
      >>> with ctx_redirect_io() as io_target:
      ...    print('how is this for io?')
      >>> io_target.getvalue()
      'how is this for io?\n'
    """
    target = f or StringIO()

    # Redirect IO to target.
    original_stdout = sys.stdout
    try:
        sys.stdout = target
        # provide an entry point for the procedure we are wrapping as well
        # as a reference to target
        yield target
    finally:
        # Restore stdio
        sys.stdout = original_stdout

redirect_io = ctx_redirect_io

#def redirect_io(f):
#    """
#    redirect all of the output to standard out to a StringIO instance,
#    which can be accessed as an attribute of the function, f.io_target
#
#    Usage Example:
#        >>> @redirect_io
#        ... def foo(x):
#        ...    print(x)
#        >>> foo('hello?')
#        >>> print(foo.io_target.getvalue())    # doctest:+NORMALIZE_WHITESPACE
#        hello?
#        >>>
#    """
#    @wraps(f)
#    def wrap(*args, **kwargs):
#        with ctx_redirect_io() as io_target:
#            wrap.io_target = io_target
#            return f(*args, **kwargs)
#    return wrap


if __name__ == '__main__':

    import doctest

    def run_tests():

        def test_redirect_io():
            msg = 'hello there?'
            with redirect_io() as f:
                print(msg)
            assert str(f.getvalue().strip()) == msg

        test_redirect_io()

    run_tests()
    print('passed')

    doctest.testmod()

    #attn('ATTENTION!')
