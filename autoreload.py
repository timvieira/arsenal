import os
import sys

from time import sleep
from threading import Thread

_win = sys.platform == "win32"

# TODO: make this a more general purpose utility
class watch(Thread):
    """
    Daemon thread with watches a file for changes
    """
    def __init__(self, mod, name=None, pause=1, verbose=True):
        Thread.__init__(self)
        self.filename = mod.__file__   # TODO: consider using debug.edit get_filename
        self.name = name or mod.__name__
        self.mod = mod
        self.pause = pause
        self.verbose = verbose
        self.setDaemon(True)
        self.start()
        self.mtimes = {}

    def run(self):
        if self.filename.endswith('.pyc') or self.filename.endswith('.pyo'):
            self.filename = self.filename[0:-1]
        if self.verbose:
            print 'autoreload module:', self.name
            print 'watching file:', self.filename
        while True:
            if self.file_changed(self.filename):
                try:
                    if self.verbose:
                        print 'reloading', self.name
                    globals()[self.name] = reload(self.mod)
                except Exception as e:
                    print 'error in:', self.filename, '... ignoring reload.'
                    print e
            sleep(self.pause)
        if self.verbose:
            print 'thread done...'

    def file_changed(self, filename):
        if not os.path.exists(filename):
            sys.stderr.write("file '%s' doens't exist..." % filename)
            return False
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if _win:
            mtime -= stat.st_ctime
        if filename not in self.mtimes:
            self.mtimes[filename] = mtime
            return False
        if mtime != self.mtimes[filename]:
            self.mtimes.clear()
            return True
        return False


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
            watch(watch_me, pause=0.1)

            assert watch_me.f() == old

            # wait a few seconds to make a change
            sleep(2)

            # make a change
            with file(filename, 'wb') as f:
                f.write(function % new)

            # wait a few seconds
            sleep(4)

            assert watch_me.f() == new

        finally:

            print 'removing temporary files...'
            try:
                os.remove('watch_me.py')
                os.remove('watch_me.pyc')
            except OSError:
                pass

        print 'done.'
    test()
