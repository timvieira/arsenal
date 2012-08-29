"""
When an exception is encountered, save context information about the exception
to a file, so that we can later invoke an editor on the last exception, bringing
it automatically at the correct file:line location.

Install this feature in your sitecustomize.py file by importing this module.
"""

import re, os, sys, traceback, subprocess
from os.path import join, isabs, realpath

__all__ = ('invoke_editor',)


def get_filename():
    return join(os.environ.get('HOME', '/tmp'), '.python_last_exception')


def atexit_handler():

    if not hasattr(sys, 'last_traceback'):
        return
    else:
        cwd = os.environ.get('PWD', '')
        fn = get_filename()

        f = open(fn, 'w')
        f.write(cwd + '\n')
        traceback.print_tb(sys.last_traceback, file=f)
        f.close()


def invoke_editor():

    try:
        f = open(get_filename())
    except IOError:
        print >> sys.stderr, "error: can't find %s" % get_filename()
        return

    fiter = iter(f)
    cwd = fiter.next().strip()
    tbtxt = list(fiter)

    # Keep the last line that matches...
    mo = None
    for line in reversed(tbtxt):
        mo = re.match('.*File "(.*)", line ([0-9]+)', line) or mo
        if mo:
            break
    else: # Not found
        return

    if mo:
        filename, lineno = mo.group(1, 2)
        lineno = int(lineno)
        if not isabs(filename):
            filename = realpath(join(cwd, filename))

    print filename, lineno
    invoke_emacs(filename, lineno)
    return 0

def invoke_emacs(filename, lineno):
    subprocess.call(['emacsclient', '-n',
                     '-e', '(find-file "%s")' % filename,
                     '-e', '(goto-line %d)' % lineno,
                     '-e', '(recenter)',
                     '-e', '(set-mark (point))',
                     '-e', '(next-line)'])


if __name__ == '__main__':
    if 'example' in sys.argv:

        # register handler
        import atexit
        atexit.register(atexit_handler)

        def example():
            import time
            print 'count down to error.'
            for i in xrange(10, 1, -1):
                print i
                time.sleep(0.1)
            1/0

        example()
    else:
        sys.exit(invoke_editor())

else:
    import atexit
    atexit.register(atexit_handler)
