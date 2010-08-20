import weakref

class ondemand(property):
    """A property that is loaded once from a function."""
    def __init__(self, fget, doc=None):
        property.__init__(self, fget=self.get, fdel=self.delete, doc=doc)
        self.loadfunc = fget
        self.values = weakref.WeakKeyDictionary()
    def get(self, obj):
        if obj not in self.values:
            self.load(obj)
        return self.values[obj]
    def load(self, obj):
        self.values[obj] = self.loadfunc(obj)
    def delete(self, obj):
        try:
            del self.values[obj]
        except:
            pass


class cached_property(object):
    """
    Lazy-loading read/write property descriptor.
    Value is stored locally in descriptor object. If value is not set when
    accessed, value is computed using given function. Value can be cleared
    by calling 'del'.
    """
    def __init__(self, func):
        self._func = func
        self._values = {}
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, obj_class):
        if obj is None:
            return obj
        if obj not in self._values or self._values[obj] is None:
            self._values[obj] = self._func(obj)
        return self._values[obj]

    def __set__(self, obj, value):
        self._values[obj] = value

    def __delete__(self, obj):
        if self.__name__ in obj.__dict__:
            del obj.__dict__[self.__name__]
        self._values[obj] = None


if __name__ == '__main__':
    from collections import defaultdict

    class Foo(object):
        def __init__(self, x):
            self.x = x
            self.log = defaultdict(int)
        @ondemand
        def my_ondemand(self):
            self.log['ondemand'] += 1
            return 'ON DEMAND'.split()        # return something mutable
        @cached_property
        def my_cached(self):
            self.log['cached_property'] += 1
            return 'CACHED PROPERTY'.split()

    def test():
        import pickle

        def checks(x):
            o = x.my_ondemand
            c = x.my_cached
            assert x.my_ondemand is o
            assert x.my_cached is c
            assert min(x.log.values()) == max(x.log.values()) == 1

        foo = Foo('XXX')
        checks(foo)
        foo.log.clear()

        print 'pickling and unpickling..'
        foo2 = pickle.loads(pickle.dumps(foo))

        # should still call both lazy properties again.
        checks(foo2)

    test()

