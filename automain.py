import sys
from misc import timeit

def automain(verbose=False, breakin=False, ultraTB=False, pdb=False):
    """
    Automatically create a very simple command-line interface.

    Note: All functions must take string arguments
    """
    import __main__ as mod
    
    if breakin:
        from debug import breakin
        breakin.enable()

    if ultraTB:
        from debug import ultraTB2
        ultraTB2.enable()

    if pdb:
        from debug.utils import enable_debug_hook
        enable_debug_hook()

    # should we print the module's docstring in the help?
    def show_help():
        print 'what do you want to do?'
        for name in dir(mod):
            obj = getattr(mod, name)
            try:
                if obj.__module__ == '__main__':
                    if obj.__doc__ is None:
                        doc = '<no documentation provided>'
                    else:
                        if verbose:
                            doc = obj.__doc__.strip()
                        else:
                            doc = obj.__doc__.strip().split('\n')[0]   # use first line

                    print '  %s:\n\t%s\n' % (name, doc)
            except AttributeError:
                pass

    try:
        action = getattr(mod, sys.argv[1])
        assert hasattr(action, '__call__')
    except (IndexError, AttributeError, AssertionError):
        show_help()
    else:
        args = tuple(sys.argv[2:])
        kw = {}  # TODO: parse keywords
        with timeit(msg='took %%.3f seconds to execute '
                        '"%s%s".' % (action.__name__, args)):
            out = action(*args, **kw)
            try:
                for x in out:
                    print x
            except TypeError:
                if out is not None:
                    print out
