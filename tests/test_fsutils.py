import os

from arsenal.fsutils import preserve_cwd


def test_preserve_cwd():
    before = os.getcwd()
    with preserve_cwd():
        os.chdir('..')
        os.chdir('..')
    assert before == os.getcwd()

    @preserve_cwd
    def foo():
        os.chdir('..')
        os.chdir('..')
    cwd_before = os.getcwd()
    foo()
    assert os.getcwd() == cwd_before
