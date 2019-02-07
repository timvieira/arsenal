"""Caching with pickle and the file system.

"""
import pickle
from path import Path as path
from arsenal.fsutils import filesize
from arsenal.timer import timeit


def load(filename, default=None, saveit=False, verbose=False):
    "Load cached item by `name`, on miss call `get` function and cached results."
    f = path(filename)
    if f.exists():
        if verbose:
            print('[load] %s, size = %s' % (f, filesize(f)))
            with timeit('[load] %s' % filename):
                with open(f) as pkl:
                    return pickle.load(pkl)
        else:
            with open(f) as pkl:
                return pickle.load(pkl)
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
            with open(filename, 'w') as pkl:
                pickle.dump(val, pkl)
            print('[save] %s, size = %s' % (filename, filesize(filename)))
    else:
        with open(filename, 'w') as pkl:
            pickle.dump(val, pkl)
    return val
