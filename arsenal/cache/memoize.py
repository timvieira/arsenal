import atexit
import shelve
import pickle as pickle

from functools import partial


# TODO:
#  * add option to pass a reference to another cache
class memoize(object):
    """ cache a function's return value to avoid recalulation """
    def __init__(self, func):
        self.func = func
        self.cache = {}
        try:
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__
        except AttributeError:
            pass

    def __get__(self, obj, objtype=None):
        "define `__get__` in case this function is a method."
        #print('  method get', obj, objtype)
        if obj is None: return self.func
        return partial(self, obj)

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            try:
                self.cache[args] = value
            except TypeError:
                # uncachable -- for instance, passing a list as an argument.
                raise TypeError('uncachable arguments %r passed to memoized function.' % (args,))
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            raise TypeError('uncachable arguments %r passed to memoized function.' % (args,))

    def __repr__(self):
        return '<memoize(%r)>' % self.func


class ShelfBasedCache(object):
    """ cache a function's return value to avoid recalulation and save cache in a shelve. """
    def __init__(self, func, key, None_is_bad=False):
        self.func = func
        self.filename = '{self.func.__name__}.shelf~'.format(self=self)
        self.cache = shelve.open(self.filename, flag='c') #, writeback=True)
        self.key = key
        self.None_is_bad = None_is_bad
        self.__name__ = 'ShelfBasedCache(%s)' % func.__name__
    def __call__(self, *args):
        p_args = self.key(args)
        value = None
        recompute = True
        if self.cache.has_key(p_args):
            recompute = False
            value = self.cache[p_args]
            if value is None and self.None_is_bad:
                recompute = True
        if recompute:
            self.cache[p_args] = value = self.func(*args)
            self.cache.sync()
        return value

def persistent_cache(key=lambda x: x, None_is_bad=False):
    def wrap(f):
        return ShelfBasedCache(f, key, None_is_bad=None_is_bad)
    return wrap



## TODO: automatically make a back-up of any previous pickles just in case the
##   save fails.  (Saving at-exit can be pretty flaky.)
class memoize_persistent(object):
    """
    cache a function's return value to avoid recalulation and save the
    cache (via pickle) at system exit so that it persists.

    WARNING: retrieves cache for functions which might not be equivalent
             if a revision is made to the code which is used to compute it.
    """
    def __init__(self, func, filename=None):
        self.func = func
        self.filename = filename or '{self.func.__name__}.cache.pkl~'.format(self=self)
        self.dirty = False
        self.key = 0
        self.cache = {}
        self.loaded = False
        atexit.register(self.save)

    def save(self):
        if self.cache and self.dirty:
            with open(self.filename, 'wb') as f:
                pickle.dump((self.cache, self.key), f)
            print('[ATEXIT] saved persistent cache for {self.func.__name__} to file "{self.filename}"'.format(self=self))
        else:
            print("[ATEXIT] found nothing to save in {self.func.__name__}'s cache.".format(self=self))

    def load(self):
        self.loaded = True
        loaded_key = None
        try:
            with open(self.filename, 'rb') as f:
                (cache, loaded_key) = pickle.load(f)
        except IOError:
            pass
        finally:
            if self.key == loaded_key:
                self.cache = cache
                #print 'loaded cache for {self.func.__name__}'.format(self=self)
            else:
                self.cache = {}
                #print 'failed to load cache for {self.func.__name__}'.format(self=self)

    def __call__(self, *args):
        # wait until you call the function to un-pickle
        if not self.loaded:
            self.load()
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            try:
                self.cache[args] = value
            except TypeError:
                # uncachable -- for instance, passing a list as an argument.
                raise TypeError('uncachable arguments %r passed to memoized function.' % (args,))
            else:
                self.dirty = True
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            raise TypeError('uncachable arguments %r passed to memoized function.' % (args,))

    def get_cached(self, *args):
        """ If result is cached return it, otherwise return `None`. """
        # wait until you call the function to un-pickle
        if not self.loaded:
            self.load()
        if args in self.cache:
            return self.cache[args]
        else:
            return None


def test_memoize():

    @memoize
    def g(x):
        return x**2

    class foo:
        def __init__(self, a):
            self.a = a
        @memoize
        def goo(self, x):
            return self.a * x
        def __repr__(self):
            return f'foo({self.a})'

    a = foo(2)
    b = foo(3)

    print('created')
    a_goo = a.goo
    print(a.goo)
    print('calling')
    assert a_goo(5) == 2*5
    assert b.goo(5) == 3*5
    print('ok')

    assert a_goo(5) == 2*5

    print('xxx')
    print(foo.goo)   # triggers method.get
    assert foo.goo(a, 4) == 2*4
    print('----')

    print(a.__class__.__dict__['goo'])        # gives the memoize instance
    print(a.__class__.__dict__['goo'].cache)  # it's hashing (obj, args)

    print('----')
    assert g(4) == 4**2    # no __get__ call here.
    print(g)
    print(g.cache)
    print('ok')


if __name__ == '__main__':
    test_memoize()
