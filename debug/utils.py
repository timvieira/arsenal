"""
Debugging utilities
"""

import re
import sys
import pdb
import inspect


def enable_debug_hook():
    "Register pdb's post-mortem debugger as the handler for uncaught exceptions."
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()

