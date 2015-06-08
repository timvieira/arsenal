"""Caching with pickle and the file system.

"""
import cPickle
from path import path
from arsenal.fsutils import filesize
from arsenal.timer import timeit


def load(filename, default=None, saveit=False, verbose=False):
    "Load cached item by `name`, on miss call `get` function and cached results."
    f = path(filename)
    if f.exists():
        if verbose:
            print '[load] %s, size = %s' % (f, filesize(f))
            with timeit('[load] %s' % filename):
                with file(f) as pkl:
                    return cPickle.load(pkl)
        else:
            with file(f) as pkl:
                return cPickle.load(pkl)
    else:
        if default is None:
            raise OSError("File not found '%s'" % filename)
        with timeit('[load] make %s' % filename):
            val = default()
        if saveit:
            save(filename, val, verbose=verbose)
        return val


def save(filename, val, verbose=False):
    "Save `val` so we can load it via `load`."
    if verbose:
        with timeit('[save] %s' % filename):
            with file(filename, 'wb') as pkl:
                cPickle.dump(val, pkl)
            print '[save] %s, size = %s' % (filename, filesize(filename))
    else:
        with file(filename, 'wb') as pkl:
            cPickle.dump(val, pkl)
    return val
