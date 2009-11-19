import os
import sys
import time

__doc__ = """

usage:

    >>> with file('watch_me.py', 'wb') as f:
    ...     f.write('f = lambda : "hello there!"')
    >>> import autoreload
    >>> import watch_me
    >>> autoreload.start_reloader(watch_me, quiet=True)
    >>> with file('watch_me.py', 'wb') as f:
    ...     f.write('f = lambda : "new message :-)"')
    >>> import time; time.sleep(2)  # give it a few seconds...
    >>> msg = watch_me.f()
    >>> print msg
    new message :-)

"""


try:
    import thread
except ImportError:
    import dummy_thread as thread

# This import does nothing, but it's necessary to avoid some race conditions
# in the threading module. See http://code.djangoproject.com/ticket/2330 .
try:
    import threading
except ImportError:
    pass

_mtimes = {}
_win = (sys.platform == "win32")


def file_changed(filename):
    global _mtimes
    global _win

    if not os.path.exists(filename):
        # print 'file doens't exist...'
        return False

    stat = os.stat(filename)
    mtime = stat.st_mtime
    if _win:
        mtime -= stat.st_ctime
    if filename not in _mtimes:
        _mtimes[filename] = mtime
        return False
    if mtime != _mtimes[filename]:
        _mtimes = {}
        return True
    return False


def start_reloader(mod):

    def reloader_thread():
        f = mod.__file__
        if f.endswith('.pyc') or f.endswith('.pyo'):
            f = f[0:-1]
        print 'watching file:', f, 'module:', mod.__name__
        while True:
            if file_changed(f) or file_changed(mod.__file__):
                print 'file %s changed.' % f
                try:
                    print 'reloading module named:', mod.__name__
                    globals()[mod.__name__] = reload(mod)
                except:
                    print 'error in:', f, '... ignoring reload.'

            time.sleep(1)
        print 'thread done...'

    thread.start_new_thread(reloader_thread, tuple())



### BROKEN: (!)
if __name__ == '__main__':

    with file('watch_me.py', 'wb') as f:
        f.write('f = lambda : "old message"')

    import watch_me
    start_reloader(watch_me)

    b4 = watch_me.f()
    print b4

    #os.remove('watch_me.py')
    with file('watch_me.py', 'wb') as f:
        f.write('f = lambda : "new message :-)"')
    #os.remove('watch_me.pyc')
    time.sleep(5)  # give it a few seconds...

#x    watch_me = reload(watch_me)

    msg = watch_me.f()
    print msg


    try:
        os.remove('watch_me.py')
        os.remove('watch_me.pyc')
    except OSError:
        pass

