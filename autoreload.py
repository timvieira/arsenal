import os
import sys
import time

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
_win = sys.platform == "win32"


def file_changed(filename):
    if not os.path.exists(filename):
        print "file '%s' doens't exist..." % filename
        return False
    stat = os.stat(filename)
    mtime = stat.st_mtime
    if _win:
        mtime -= stat.st_ctime
    if filename not in _mtimes:
        _mtimes[filename] = mtime
        return False
    if mtime != _mtimes[filename]:
        _mtimes.clear()
        return True
    return False


def start_reloader(mod, sleepsec=1, verbose=True):

    def reloader_thread():
        f = mod.__file__
        if f.endswith('.pyc') or f.endswith('.pyo'):
            f = f[0:-1]
        if verbose:
            print 'autoreload module:', mod.__name__
            print 'watching file:', f
        while True:
            if file_changed(f) or file_changed(mod.__file__):
                try:
                    if verbose:
                        print 'reloading', mod.__name__
                    globals()[mod.__name__] = reload(mod)
                except Exception as e:
                    print 'error in:', f, '... ignoring reload.'
                    print e
            time.sleep(sleepsec)
        if verbose:
            print 'thread done...'

    thread.start_new_thread(reloader_thread, tuple())


if __name__ == '__main__':

    def test():
        old = "old message"
        new = "new message :-)"
        function = 'f = lambda : %r'
        filename = 'watch_me.py'
    
        try:
            with file(filename, 'wb') as f:
                f.write(function % old)
    
            import watch_me
            start_reloader(watch_me)
    
            assert watch_me.f() == old
    
            # wait a few seconds to make a change
            time.sleep(2)
    
            # make a change
            with file(filename, 'wb') as f:
                f.write(function % new)
    
            # wait a few seconds
            time.sleep(5)
    
            assert watch_me.f() == new
    
        finally:
            try:
                os.remove('watch_me.py')
                os.remove('watch_me.pyc')
            except OSError:
                pass

    test()
