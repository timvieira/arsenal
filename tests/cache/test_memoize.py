from arsenal.cache.memoize import memoize


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

    a_goo = a.goo
    assert a_goo(5) == 2*5
    assert b.goo(5) == 3*5

    assert a_goo(5) == 2*5

    assert foo.goo(a, 4) == 2*4

    assert g(4) == 4**2
