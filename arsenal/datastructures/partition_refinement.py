"""
`PartitionRefinement` is a data structure for representing a partition of a
set.  Unlike the better-known `UnionFind` data structure, which *merges* sets,
the `PartitionRefinement` data structure performs the "dual" operation of
*splitting* sets.

Important use cases:
  - Efficient DFA minimization

References:
  https://en.wikipedia.org/wiki/Partition_refinement

Original version by Ryan Cotterell

"""

import numpy as np
from collections import defaultdict
from arsenal import colors


def stable(f, P):
    "Is partition P stable?"
    D = {}
    for n, B in enumerate(P):
        for q in B:
            D[q] = n
    for B in P:
        for p in B:
            for q in B:
                if D[f[p]] != D[f[q]]:
                    return False
    return True


def split(S, P):
    return frozenset(P & S), frozenset(P-S)


def hopcroft(f, P):

    # compute the pre-image of f
    finv = defaultdict(set)
    for n in f:
        finv[f[n]].add(n)

    stack = list(P)

    while stack: # empties in O(log n) steps
        S = stack.pop()
        R = set() # new refinement

        # compute subset of the pre-image in O(n) time
        Sinv = set.union(*[finv[x] for x in S])

        for B in P: # entire loop runs in O(n) time
            X, Y = split(Sinv, B) # runs in O(|B|) time

            if len(X) > 0 and len(Y) > 0:
                # X, Y are now part of the refinement
                R.add(X)
                R.add(Y)

                # Hopcroft's speed-up to the slower algorithm is that we
                # only need to enqueue the smaller set.
                if len(X) < len(Y):
                    stack.append(X)
                else:
                    stack.append(Y)
            else:
                # Q remains part of the refinement
                R.add(B)
        P = R

    return frozenset(P)


def slow(f, P):

    # compute the pre-image of f
    finv = defaultdict(set)
    for n in f:
        finv[f[n]].add(n)

    stack = list(P)

    while stack: # empties in O(n) steps
        S = stack.pop()
        R = set() # new refinement

        # compute subset of the pre-image in O(n) time
        Sinv = set.union(*[finv[x] for x in S])

        for B in P: # entire loop runs in O(n) time
            X, Y = split(Sinv, B) # runs in O(|B|) time

            if len(X) > 0 and len(Y) > 0:
                # X, Y are now part of the refinement
                R.add(X)
                R.add(Y)

                # X, Y become future splitters
                stack.append(X)
                stack.append(Y)
            else:
                # Q remains part of the refinement
                R.add(B)
        P = R

    return frozenset(P)


def test_partition():
    import random

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
        #print(want)

    print(colors.ok)


if __name__ == '__main__':
    from arsenal import testing_framework
    testing_framework(globals())
