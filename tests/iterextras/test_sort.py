import itertools

import numpy as np

from arsenal.iterextras.sort import sorted_product


def test_sorted_product():
    class WeightedTuple:
        def __init__(self, w, *key):
            self.key = key
            self.w = w
        def __lt__(self, other):
            return (self.w, self.key) < (other.w, other.key)
        def __eq__(self, other):
            return (self.w, self.key) == (other.w, other.key)
        def __mul__(self, other):
            return LWeightedTuple(self.w*other.w, self, other)
        def __add__(self, other):
            return LWeightedTuple(self.w+other.w, self, other)
        def __iter__(self):
            return iter((self.w, self.key))
        def __repr__(self):
            return repr((self.w, self.key))

    class LWeightedTuple(WeightedTuple):
        def __init__(self, w, a, b):
            self.w = w
            self.a = a
            self.b = b
        @property
        def key(self):
            return self.a.key + self.b.key

    def wprod(xs):
        return np.prod([WeightedTuple(x, x) for x in xs])

    def check(iters):
        for p in [np.prod, np.sum, tuple, wprod]:
            want = list(sorted(p(x) for x in itertools.product(*iters)))
            have = list(sorted_product(p, *iters))
            assert have == want

    check([
        (.1, .4, 0.5),
        (0.09, 0.11, 0.8),
        (0.111, .3, 0.6),
    ])
    check([
        (1, 2, 3),
        (4, 7, 11),
    ])
    check([
        (0.01, .4, 0.5),
        (0.11, 0.8),
        (0.6,),
    ])
    check([
        (1, 2, 3, 100),
        (4, 7, 9),
        (14, 17, 19),
        (24, 27, 29),
    ])
