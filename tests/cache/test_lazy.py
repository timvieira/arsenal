import pickle
from collections import defaultdict

from arsenal.cache.lazy import lazy


class Foo(object):
    def __init__(self, x):
        self.x = x
        self.log = defaultdict(int)
    @lazy
    def my_ondemand(self):
        self.log['ondemand'] += 1
        return 'ON DEMAND'.split()
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


def test_lazy():
    def checks(x):
        o = x.my_ondemand
        c = x.my_cached
        l = x.my_lazy
        assert x.my_ondemand is o
        assert x.my_cached is c
        assert x.my_lazy is l
        assert min(x.log.values()) == max(x.log.values()) == 1

        ll = x.my_lazy_list
        assert ll == list(range(10)), ll
        assert ll is x.my_lazy_list

        assert all(v == 1 for v in x.log.values())

    foo = Foo('XXX')
    checks(foo)
    foo.log.clear()

    foo2 = pickle.loads(pickle.dumps(foo))

    # should still call both lazy properties again.
    assert not foo2.log
