
import sys, functools
from StringIO import StringIO
from contextlib import contextmanager

@contextmanager
def ctx_redirect_io():

    target = StringIO()

    # Redirect IO to self.target.
    original_stdout = sys.stdout
    sys.stdout = target

    # provide an entry point for the procedure we are wrapping
    yield target

    # Restore stdio and close the file.
    sys.stdout = original_stdout


def redirect_io(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        with ctx_redirect_io() as io_target:
            wrap.io_target = io_target
            return f(*args, **kwargs)
    return wrap


if __name__ == '__main__':

    with ctx_redirect_io() as io_target:
        print 'how is this for io?'
    print 'redirected>', repr(io_target.getvalue())


    @redirect_io
    def foo(x):
        """ hey there. """
        print x

    foo('hello there?')
    print 'redirected>', foo.io_target.getvalue()
