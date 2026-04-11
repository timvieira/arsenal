import random

import numpy as np

from arsenal.datastructures.partition_refinement import slow, hopcroft, stable


def test_partition():
    for _ in range(25):
        N = 50

        # create random total function
        f = dict(zip(range(N), random.choices(range(N), k=N)))

        # create random partition
        i = random.randint(2, N-1)
        P = np.random.permutation(range(N))
        P = { frozenset(P[:i]), frozenset(P[i:]) }

        want = slow(f, P)
        have = hopcroft(f, P)
        assert want == have
        assert stable(f, have)
