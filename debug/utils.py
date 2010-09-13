"""
Debugging utilities
"""

import re
import sys
import inspect
import traceback

# try to use IPython's fancy debugger if available
try:
    from IPython.Debugger import Pdb
    from IPython.Shell import IPShellEmbed
    ip = __IPYTHON__ = IPShellEmbed([])
    def set_trace():
        callerframe = sys._getframe().f_back
        Pdb().set_trace(callerframe)
    def pm():    
        p = Pdb()
        p.reset()
        p.interaction(None, sys.last_traceback)    
except ImportError:
    from pdb import set_trace, pm, Pdb


def enable_debug_hook():
    "Register pdb's post-mortem debugger as the handler for uncaught exceptions."
    def debug_hook(*args):
        sys.__excepthook__(*args)
        pm()
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
    print debug_expr_fmt % (cf.f_code.co_name, expr, val)


def debugx(obj):
    """
    I often write debugging print statements which look like
      >>> somevar = 'somevalue'
      >>> print 'somevar:', somevar
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
    print code + ':', obj


# TIMV: would it be possibe to change this function to work without raising
#       and exception?
def framedump():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.

    Note: this function does not work when there is no exception.
    """

    # Move to the frame where the exception occurred, which is often not the
    # same frame where the exception was caught.
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next

    # get the stack frames
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()

    print 'Traceback:'
    print '=========='
    print traceback.format_exc()

    print 'Locals by frame:'
    print '================'
    for frame in stack:
        print 'Frame %s in %s at line %s' % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
        for key, value in frame.f_locals.iteritems():
            print '\t%10s = %r' % (key, value)

        print
        print


if __name__ == '__main__':
    import doctest
    doctest.testmod()

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
                return_value.append("0" * (4 - len(thing)) + thing)
            return return_value

        print '============================================================'
        print 'The usual information'
        print '============================================================'
        # First, show the information we get from a normal traceback.print_exc().
        try:
            pad4(data)
        except:
            traceback.print_exc()

        print
        print '============================================================'
        print 'Tracebacks with the frame dump'
        print '============================================================'

        # With our new function it is to see the bad data that
        # caused the problem. The variable 'thing' has the value 3, so we know
        # that the TypeError we got was because of that. A quick look at the
        # value for 'data' shows us we simply forgot the quotes on that item.
        try:
            pad4(data)
        except:
            framedump()

    example()
