import os, contextlib, functools

@contextlib.contextmanager
def preserve_cwd():
    cwd = os.getcwd()
    yield
    os.chdir(cwd)

def preserve_cwd_dec(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        with preserve_cwd():
            return f(*args, **kwargs)
    return wrap

def run_tests():

    def nasty_function():
        print '<nasty_function>'
        os.chdir('..')
        print '  cd ..'
        print '  cwd:', os.getcwd()
        os.chdir('..')
        print '  cd ..'
        print '  cwd:', os.getcwd()
        print '</nasty_function>'

    def test_cwd_ctx_manager():
        print 'test_cwd_ctx_manager:'
        before = os.getcwd()
        with preserve_cwd():
            nasty_function()
        assert before == os.getcwd()

    def test_preserve_cwd_dec():
        print 'test_preserve_cwd_dec:'
        @preserve_cwd_dec
        def foo():
            nasty_function()
        cwd_before = os.getcwd()
        foo()
        assert os.getcwd() == cwd_before

    test_cwd_ctx_manager()
    test_preserve_cwd_dec()


if __name__ == '__main__':
    run_tests()



