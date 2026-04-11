import numpy as np

from arsenal.iterextras.sorted_intersection import sorted_intersection


def test_sorted_intersection():
    for _ in range(20):
        n = 2**10
        m = 20

        U = range(max(n, m) * 5)
        A = sorted(np.random.choice(U, n, replace=False))
        B = sorted(np.random.choice(U, m, replace=False))

        want = sorted(set(A) & set(B))
        have = list(sorted_intersection(A, B))

        assert have == want
