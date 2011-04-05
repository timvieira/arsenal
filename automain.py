import sys
from inspect import isfunction, ismethod, getargs, getargspec, formatargspec
from optparse import OptionParser
from pprint import pprint
from collections import defaultdict

'''
if obj.__doc__ is None:
    doc = '...'
else:
    if verbose:
        doc = obj.__doc__.strip()
    else:
        doc = obj.__doc__.strip().split('\n')[0]   # use first line
print '   ', doc
'''

def usage(obj):
    name = obj.__name__
    signature = call_signature(obj) or '%s(???)' % name
    doc = '    ' + (getattr(obj, '__doc__', '...') or '...').strip()
    return '\n'.join([signature, doc])

def call_signature(obj, oname=''):
    """
    Return the definition header for any callable object.

    If any exception is generated, None is returned instead and the
    exception is suppressed.
    """
    oname = oname or obj.__name__
    if isfunction(obj):
        func_obj = obj
    elif ismethod(obj):
        func_obj = obj.im_func
    else:
        # obj is not a Python function'
        return None
    args, varargs, varkw = getargs(func_obj.func_code)
    return oname + formatargspec(args, varargs, varkw, func_obj.func_defaults)


def automain(argv=None, verbose=False, breakin=False, ultraTB=False, pdb=False,
             timemsg=False, available=None):
    """
    Automatically create a very simple command-line interface.

    Note: All functions must take string arguments
    """
    import __main__ as mod
    argv = argv or sys.argv

    try:
        if breakin:
            from debug import breakin
            breakin.enable()

        if ultraTB:
            from debug import ultraTB2
            ultraTB2.enable(include_vars=False)

        if pdb:
            from debug.utils import enable_debug_hook
            enable_debug_hook()

        if timemsg:
            from humanreadable import print_elapsed_time
            print_elapsed_time()

    except ImportError:
        pass

    names = list(sorted(available or [x for x in dir(mod) if x not in ('automain', 'usage', 'call_signature')]))

    # should we print the module's docstring in the help?
    def show_help():
        print 'what do you want to do?'
        print
        for name in names:
            try:
                # we might have been passed objects instead of names
                if isinstance(name, basestring):
                    obj = getattr(mod, name)
                else:
                    obj = name
                    name = obj.__name__
                if not obj.__module__ == '__main__':
                    continue
                if not hasattr(obj, '__call__'):
                    continue
            except AttributeError:
                continue
            else:
                print usage(obj)
                print

    try:
        action = getattr(mod, argv[1])
        assert hasattr(action, '__call__')
    except (IndexError, AttributeError, AssertionError):
        show_help()
    else:
        args = list(argv[2:])

        parser = OptionParser()
        #parser.allow_interspersed_args = False
        spec = getargspec(action)

        if spec.defaults is not None:
            for default, arg in zip(reversed(spec.defaults), reversed(spec.args)):  # args with default values
                longname = '--' + arg
                #if isinstance(default, bool):   # XXX: this not the right semantics.
                #    if default == False:
                #        parser.add_option(longname, action="store_true", default=False)
                #    else:
                #        parser.add_option(longname, action="store_false", default=True)
                #else:
                parser.add_option(longname, default=default)
                
        (kw, args) = parser.parse_args(args)

        # TODO: need a better usage message with shows positional arguments

        # minimum non keyword args
        if len(args) < len(spec.args) - len(spec.defaults or []):
            parser.print_help()
            return

        kw = kw.__dict__

        out = action(*args, **kw)
        if isinstance(out, basestring):
            print out

        elif isinstance(out, dict):
            if isinstance(out, defaultdict):
                out = dict(out)
            pprint(out)

        else:
            try:
                out = iter(out)
            except TypeError:
                if out is not None:
                    print out
            else:
                for x in out:
                    print x


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].endswith('py'):
        sys.argv = sys.argv[1:]
        execfile(sys.argv[0])
        # TODO: remove automain from the list
        automain()

