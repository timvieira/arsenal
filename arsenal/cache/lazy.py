# TODO:
#  - consider allowing lazy things to depend on one another

from types import GeneratorType

class lazy(object):
    """
    Lazily load a property defined by a method. The method wrapped is called
    at most once to retrieve the result and the result is reused. If the method
    is a generator, the value is stored as a list.

    Note: instances must have a `__dict__` attribute in order for this property
    to work, i.e. no '__slots__' class attribute.

    Implementation detail: this is not implemented as a data descriptor so that
    we can completely avoid the function call overhead. If one choses to invoke
    `__get__` by hand the property will still work as expected because the
    lookup logic is replicated in `__get__` for manual invocation.
    """

    def __init__(self, func):
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(self, obj, type_=None):
        if obj is None:
            return self
        try:
            value = obj.__dict__[self.__name__]
        except KeyError:
            value = self.func(obj)
            if isinstance(value, GeneratorType):   # store generators as lists
                value = list(value)
            obj.__dict__[self.__name__] = value
        return value

    def __set__(self, obj, value):
        raise NotImplementedError

    def __delete__(self, obj):
        raise NotImplementedError


if __name__ == '__main__':
    from collections import defaultdict

    class Foo(object):
        def __init__(self, x):
            self.x = x
            self.log = defaultdict(int)       # track the number of calls to our cached properties/methods
        @lazy
        def my_ondemand(self):
            self.log['ondemand'] += 1
            return 'ON DEMAND'.split()        # return something mutable
        @lazy
        def my_cached(self):
            self.log['cachedproperty'] += 1
            return 'CACHED PROPERTY'.split()
        @lazy
        def my_lazy(self):
            self.log['my_lazy'] += 1
            return 'LAZY PROPERTY'.split()
        @lazy
        def my_lazy_list(self):
            self.log['my_lazy_list'] += 1
            for i in range(10):
                yield i

    def test():
        import pickle

        def checks(x):
            o = x.my_ondemand
            c = x.my_cached
            l = x.my_lazy
            assert x.my_ondemand is o
            assert x.my_cached is c
            assert x.my_lazy is l
            print('x.log:', x.log, sep=' ')
            assert min(x.log.values()) == max(x.log.values()) == 1

            ll = x.my_lazy_list
            assert ll == list(range(10)), ll
            assert ll is x.my_lazy_list

            print(x.log)
            assert all(v == 1 for v in x.log.values())

        foo = Foo('XXX')
        checks(foo)
        foo.log.clear()

        print('pickling and unpickling..')
        foo2 = pickle.loads(pickle.dumps(foo))

        # should still call both lazy properties again.
        assert not foo2.log

    test()
