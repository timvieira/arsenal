from scipy.special import comb as binom, factorial

from arsenal.maths.combinatorics.basics import (
    sumsto, sample, kleene, powerset, permute, trees, catalan,
    flatten, segmentations,
)


def _length(xs):
    return sum(1 for _ in xs)


def test_sumsto():
    for n in range(8):
        for k in range(n+1):
            N = 0
            for js in sumsto(n, k):
                N += 1
                assert sum(js) == n
                assert len(js) == k
                assert all(j >= 0 for j in js)

            have = N
            want = binom(n+k-1, n)
            assert have == want


def test_sample():
    def check(N, K):
        S = range(N)
        assert binom(N, K) == _length(sample(S, K, ordered=0, replace=0))
        assert binom(N, K) * factorial(K) == _length(sample(S, K, ordered=1, replace=0))
        assert N**K == _length(sample(S, K, ordered=1, replace=1))

    check(5, 3)
    check(5, 5)
    check(5, 0)


def test_kleene():
    from arsenal.iterextras import take

    assert (list(take(10, map(''.join, kleene('01'))))
            == ['', '0', '1', '00', '01', '10', '11', '000', '001', '010'])

    assert (list(map(''.join, kleene('01', n=3)))
            == ['', '0', '1', '00', '01', '10', '11', '000', '001', '010',
                '011', '100', '101', '110', '111'])

    assert (list(map(''.join, kleene('a', n=4)))
            == ['', 'a', 'aa', 'aaa', 'aaaa'])

    assert (list(map(''.join, kleene('', n=4)))
            == [''])

    assert _length(powerset(range(5))) == 2**5
    assert _length(permute(range(5))) == factorial(5)


def test_trees():

    _catalan = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786,
                208012, 742900, 2674440]

    for n in range(1, len(_catalan)):
        assert _catalan[n] == catalan(n), [n, _catalan[n], catalan(n)]

    def check(S, n):
        A = list(trees(S))
        for x in A:
            assert tuple(flatten(x)) == tuple(S)
        assert _length(A) == catalan(n-1)

    for n in range(2, 10):
        check(range(n), n)


def test_segmentations():
    def check(S):
        A = list(segmentations(S))
        for i, p in enumerate(sorted(A)):
            assert ''.join(''.join(s) for s in p) == ''.join(S), S
        assert len(A) == 2 ** (len(S) - 1)
        assert len(A) == len(set(A))

    for n in range(2, 10):
        check(tuple(map(str, range(n))))
