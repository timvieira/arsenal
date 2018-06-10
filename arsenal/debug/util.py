"""
Debugging utilities.
"""

import re
import sys
import inspect
import traceback


#from arsenal.debug import saverr  # registers hook
try:
    from IPython import embed as ip
except ImportError:
    try:
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
    except ImportError:
        from IPython.terminal.embed import InteractiveShellEmbed

    def ip(banner1='', **kw):
        shell = InteractiveShellEmbed.instance(banner1=banner1, **kw)
        shell(header='', stack_depth=2)


def enable_ultratb(mode='Context', **kwargs):
    from IPython.core import ultratb
    sys.excepthook = ultratb.FormattedTB(mode=mode, **kwargs)

# TODO: look IPython's debugging stuff..
# http://ipython.org/ipython-doc/dev/api/generated/IPython.core.debugger.html
from IPython.core.debugger import Tracer
set_trace = lambda: Tracer()()


#from IPython.Debugger import Pdb
from pdb import set_trace, pm, Pdb


def enable_debug_hook():
    "Register pdb's post-mortem debugger as the handler for uncaught exceptions."
    def debug_hook(*args):
        sys.__excepthook__(*args)
        pm()
    sys.excepthook = debug_hook


enable_pm = enable_debug_hook


def dumpobj(o, callables=False, private=False):
    """
    >>> class A(object):
    ...     x = 10
    ...     def __init__(self, y):
    ...         self.y = y
    ...     def span(self):
    ...         pass
    ...     def __repr__(self):
    ...         return 'A(%r, %r)' % (self.x, self.y)
    ...

    >>> dumpobj(A('hello'))
    A(10, 'hello')
    instance of: A
                       x: int
                       y: str

    >>> dumpobj(A('hello'), callables=0, private=True)
    A(10, 'hello')
    instance of: A
                __dict__: dict
                 __doc__: NoneType
              __module__: str
             __weakref__: NoneType
                       x: int
                       y: str
    """
    print(repr(o))
    print('instance of:', type(o).__name__)
    for a in dir(o):
        if not callables and callable(getattr(o, a)):
            continue
        if not private and a.startswith('__'):
            continue
        try:
            print('%20s: %s' % (a, type(getattr(o,a)).__name__))
        except:
            pass


def debug(s, *args, **kwargs):
    """
    >>> def foo():
    ...     bar = 'world'
    ...     debug('hello {bar}')
    >>> foo()
    hello world
    """
    c_frame = inspect.getouterframes(inspect.currentframe(), 1)[1][0]
    c_args, c_varargs, c_varkw, c_locals = inspect.getargvalues(c_frame)
    d = dict(c_locals)
    d.update(kwargs)
    print(s.format(*args, **d))


debug_expr_fmt = '[DEBUG:%s] %s -> %r'

# borrowed from IPython
def debug_expr(expr):
    """
    Evaluate and print the value of a string representing a python expression
    in the caller's frame.

    Takes an expression, evaluates it in the caller's frame and prints both
    the given expression and the resulting value (as well as a debug mark
    indicating the name of the calling function.  The input must be of a form
    suitable for eval().

    >>> def foo():
    ...     x = 15
    ...     debug_expr('x')
    ...     debug_expr('x**2 + 2*x + 3')
    ...     f = lambda x: x**2
    ...     debug_expr('f(x)')

    >>> foo()
    [DEBUG:foo] x -> 15
    [DEBUG:foo] x**2 + 2*x + 3 -> 258
    [DEBUG:foo] f(x) -> 225
    """
    cf = sys._getframe(1)   # caller frame
    val = eval(expr, cf.f_globals, cf.f_locals)
    print(debug_expr_fmt % (cf.f_code.co_name, expr, val))


def debugx(obj):
    """
    I often write debugging print statements which look like
      >>> somevar = 'somevalue'
      >>> print('somevar:', somevar)
      somevar: somevalue

    What this function attempts to do is provide a shortcut
      >>> debugx(somevar)
      somevar: somevalue

    Note: that we do not need to pass strings to this function.
    >>> def foo():
    ...     x = 15
    ...     debugx(x)
    ...     debugx(x**2 + 2*x + 3)
    ...     f = lambda x: x**2
    ...     debugx(f(x))

    >>> foo()
    x: 15
    x**2 + 2*x + 3: 258
    f(x): 225

    Warning: this should only be used for debugging because it relies on
    introspection, which can be really slow and sometimes even buggy.
    """
    cf = sys._getframe(1)
    ctx_lines = inspect.getframeinfo(cf).code_context
    code = ''.join(map(str.strip, ctx_lines))
    code = re.sub('debugx\((.*)\)', r'\1', code)
    print(code + ':', obj)


# TIMV: would it be possibe to change this function to work without raising
#       and exception?
def framedump():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame. If this function is called when an exception
    has been thrown the framedump will start at the origin of the exception
    not where it was caught.
    """

    # Move to the frame where the exception occurred, which is often not the
    # same frame where the exception was caught.
    tb = sys.exc_info()[2]
    if tb is not None:
        while 1:
            if not tb.tb_next:
                break
            tb = tb.tb_next
        f = tb.tb_frame
    else:                             # no exception occurred
        f = sys._getframe()

    # get the stack frames
    stack = []
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()

    print('Traceback:')
    print('==========')
    print(traceback.format_exc())

    print('Locals by frame:')
    print('================')
    for frame in stack:
        print('Frame %s in %s at line %s' % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno))
        for key, value in frame.f_locals.items():
            print('%20s = %r' % (key, value))

        print()
        print()


if __name__ == '__main__':
    import doctest

    def example():
        """
        A simple example where this approach comes in handy.

        Basically, we have a simple function which manipulates all the
        strings in a list. The function doesn't do any error checking, so when
        we pass a list which contains something other than strings, we get an
        error.
        """

        data = ["1", "2", 3, "4"]  # Typo: We 'forget' the quotes on data[2]
        def pad4(seq):
            """Pad each string in seq with zeros, to four places."""
            return_value = []
            for thing in seq:
                return_value.append("0" * (4 - len(thing)) + thing)   # intensionally buggy
            return return_value

        print('============================================================')
        print('The usual information')
        print('============================================================')
        # First, show the information we get from a normal traceback.print_exc().
        try:
            pad4(data)
        except:
            traceback.print_exc()

        print()
        print('============================================================')
        print('Tracebacks with the frame dump')
        print('============================================================')

        # With our new function it is to see the bad data that
        # caused the problem. The variable 'thing' has the value 3, so we know
        # that the TypeError we got was because of that. A quick look at the
        # value for 'data' shows us we simply forgot the quotes on that item.

        if 1:
            try:
                pad4(data)
            except:
                framedump()
        else:
#            pad4(data)
            framedump()

    example()

    import doctest
    doctest.testmod()
