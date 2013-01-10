import sys
from inspect import isfunction, ismethod, getargs, getargspec, formatargspec
from optparse import OptionParser   # TODO: use argparse
from pprint import pprint
from collections import defaultdict
from debug import ip

def usage(obj):
    name = obj.__name__.split('.')[-1]
    signature = call_signature(obj) or '%s(???)' % name
    doc = '    ' + getdoc(obj)   # todo: indent
    return '\n'.join([signature, doc])


def getdoc(obj, indent=0):
    return (getattr(obj, '__doc__', '') or '').strip()


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
             timemsg=False, available=None, mod=None, main_only=False):
    """
    Automatically create a very simple command-line interface.

    Note: All functions must take string arguments
    """

    if not mod:
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


    if available:
        filterfn = None
    else:
        def filterfn(obj):
            try:
                if not obj.__module__ == '__main__' and main_only:
                    return False
                if not hasattr(obj, '__call__'):
                    return False
            except AttributeError:
                return False
            else:
                name = obj.__name__
                return name not in ('automain', 'usage', 'call_signature') and not name.startswith('_')
        available = dir(mod)
    objects = [getattr(mod, x) if isinstance(x, basestring) else x for x in available]
    objects = list(sorted(filter(filterfn, objects), key=lambda x: x.__name__))


    # should we print the module's docstring in the help?
    def show_help(objects):
        print
        for obj in objects:
            print usage(obj)
            print

    try:
        action = getattr(mod, argv[1])
        assert hasattr(action, '__call__')
    except (IndexError, AttributeError, AssertionError):
        show_help(objects)
    else:
        args = list(argv[2:])

        parser = OptionParser()
        #parser.allow_interspersed_args = False
        spec = getargspec(action)

        if spec.defaults:
            for default, arg in zip(reversed(spec.defaults), reversed(spec.args)):  # args with default values
                longname = '--' + arg
                #if isinstance(default, bool):   # XXX: this not the right semantics.
                #    if default == False:
                #        parser.add_option(longname, action="store_true", default=False)
                #    else:
                #        parser.add_option(longname, action="store_false", default=True)
                #else:
                parser.add_option(longname, default=default)

        parser.usage = '%s [options] %s' % (action.__name__, ' '.join(spec.args)) \
            + '\n\n    ' + getdoc(action)

        (kw, args) = parser.parse_args(args)

        # TODO: need a better usage message which shows positional arguments

        # minimum non-keyword args
        if len(args) < len(spec.args) - len(spec.defaults or []):
            parser.print_help()
            return

        kw = kw.__dict__

        # call function
        out = action(*args, **kw)

        # pretty-print result
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
    if len(sys.argv) > 1 and sys.argv[1].endswith('.py'):
        sys.argv = sys.argv[1:]
        execfile(sys.argv[0])
        automain()
