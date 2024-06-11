import numpy as np
import matplotlib.pyplot as pl

from arsenal.maths import compare, random_dist
from collections import Counter
from arsenal.maths.combinatorics import permute
from arsenal.timer import timers

# XXX: warning some of these implementations may not be shipped with the
# package.  Also be sure to compile with Cython.
from arsenal.datastructures.heap.sumheap  import SumHeap as SumHeap1
from arsenal.datastructures.heap.sumheap2 import SumHeap as SumHeap2
from arsenal.datastructures.heap.sumheap3 import SumHeap as SumHeap3


def p_perm(w, z):
    "The probability of a permutation `z` under the sampling without replacement scheme."
    n = len(w); k = len(z)
    assert 0 < k <= n
    wz = w[np.array(z, dtype=int)]
    W = wz[::-1].cumsum()
    return np.prod(wz / W)


def swor_heap1(w, R):
    n = len(w)
    z = np.zeros((R, n), dtype=int)
    for r in range(R):
        h = SumHeap1(w)
        z[r] = h.swor(n)
    return z


def swor_heap2(w, R):
    n = len(w)
    z = np.zeros((R, n), dtype=int)
    for r in range(R):
        h = SumHeap2(w)
        z[r] = h.swor(n)
    return z


def swor_heap3(w, R):
    n = len(w)
    z = np.zeros((R, n), dtype=int)
    for r in range(R):
        h = SumHeap3(w)
        z[r] = h.swor(n)
    return z


def counts(S):
    "empirical distribution over z"
    c = Counter()
    m = len(S)
    for s in S:
        c[tuple(s)] += 1 / m
    return c


def test():
    methods = [
        swor_heap1,
#        swor_heap2,
        swor_heap3,
    ]

    R = 50_000
    v = random_dist(4)

    S = {f.__name__: f(v, R) for f in methods}

    D = {name: counts(S[name]) for name in S}

    R = {}
    n = len(v)
    for z in permute(range(n)):
        R[z] = p_perm(v, z)
        for d in D.values():
            d[z] += 0

    # Check that p_perm sums to one.
    np.testing.assert_allclose(sum(R.values()), 1)
    for name, d in sorted(D.items()):
        compare(R, d)#.show(title=name);

    T = timers()
    R = 50
    for i in range(1, 15):
        n = 2**i
        #print('n=', n, 'i=', i)
        for _ in range(R):
            v = random_dist(n)
            np.random.shuffle(methods)
            for f in methods:
                name = f.__name__
                with T[name](n = n):
                    S = f(v, R = 1)
                assert S.shape == (1, n)   # some sort of sanity check
    print('done')

    fig, ax = pl.subplots(ncols=2, figsize=(12, 5))
    T.plot_feature('n', ax=ax[0])
    fig.tight_layout()
    T.plot_feature('n', ax=ax[1]); ax[1].set_yscale('log'); ax[1].set_xscale('log')
    T.compare()

    pl.show()

if __name__ == '__main__':
    test()
