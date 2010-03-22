import shelve
import cPickle as pickle
from functools import wraps


class ShelfBasedCache(object):
    """ cache a function's return value to avoid recalulation and save cache in a shelve. """
    def __init__(self, func, key):
        self.func = func
        self.filename = '{self.func.__name__}.shelf~'.format(self=self)
        self.cache = shelve.open(self.filename) #, writeback=True)
        self.key = key
        self.__name__ = 'ShelfBasedCache(%s)' % func.__name__
    def __call__(self, *args):
        p_args = self.key(args)

        if self.cache.has_key(p_args):
            return self.cache[p_args]
        else:
            self.cache[p_args] = value = self.func(*args)
            self.cache.sync()
            return value
    def __del__(self):
        self.cache.close()

def persistent_cache(key):
    def wrap(f):
        return ShelfBasedCache(f, key)
    return wrap


# TODO:
#  * add option to pass a reference to another cache (maybe memcached client)
class memoize(object):
    """ cache a function's return value to avoid recalulation """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            if args in self.cache:
                return self.cache[args]
            else:
                self.cache[args] = value = self.func(*args)
                return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
    def __repr__(self):
        """ Return the function's docstring. """
        return self.func.__doc__


## TODO: automatically make a back-up of the pickle
class memoize_persistent(object):
    """
    cache a function's return value to avoid recalulation and save the
    cache (via pickle) at system exit so that it persists.

    WARNING: retrieves cache for functions which might not be equivalent
             if a revision is made to the code which is used to compute it.
    """
    def __init__(self, func):
        self.func = func
        self.filename = '{self.func.__name__}.cache.pkl~'.format(self=self)
        self.dirty = False
        self.key = 0
        self.cache = {}
        self.loaded = False
        atexit.register(self.save)

    def save(self):
        if self.cache and self.dirty:
            pickle.dump((self.cache, self.key), file(self.filename,'wb'))
            print '[ATEXIT] saved persistent cache for {self.func.__name__} to file "{self.filename}"'.format(self=self)
        else:
            print "[ATEXIT] found nothing to save in {self.func.__name__}'s cache.".format(self=self)

    def load(self):
        self.loaded = True
        loaded_key = None
        try:
            (cache, loaded_key) = pickle.load(file(self.filename,'r'))
        except IOError:
            pass
        finally:
            if self.key == loaded_key:
                self.cache = cache
                print 'loaded cache for {self.func.__name__}'.format(self=self)
            else:
                self.cache = {}
                print 'failed to load cache for {self.func.__name__}'.format(self=self)

    def __call__(self, *args):
        # wait until you call the function to un-pickle
        if not self.loaded:
            self.load()

        try:
            if args in self.cache:
                return self.cache[args]
            else:
                self.dirty = True
                self.cache[args] = value = self.func(*args)
                return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            raise TypeError('uncachable instance passed to memoized function.')
