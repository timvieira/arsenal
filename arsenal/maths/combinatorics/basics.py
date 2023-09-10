# TODO: This module should move into iterextras since it is focused on
# iterators, which are not specific to mathematics.


from itertools import product
from scipy.special import comb as binom, factorial
from arsenal import colors
import itertools



def sample(S, k, ordered, replace):
    S = tuple(S)

    if k == 0:
        yield ()
    else:
        for i, s in enumerate(S):

            if     ordered and     replace: X = S[:i] + S[i:]    # string
            if     ordered and not replace: X = S[:i] + S[i+1:]  # select
            if not ordered and     replace: X =         S[i:]    # ????
            if not ordered and not replace: X =         S[i+1:]  # choose

            for x in sample(X, k-1, ordered, replace):
                yield x + (s,)


def select(S, k):
    "Ordered subsets of size k"
    return sample(S, k, ordered=True, replace=False)


def choose(S, k):
    """
    Enumerate unordered subsets of size k from the set S.

    S does not have to be a set, it can be ordered.  The elements returned will each be a k-tuple.

    If `S` is an ordered collection, then the k-tuples returned by this iterator
    will use the sample order.

    """
    return sample(S, k, ordered=False, replace=False)


def permute(S):
    "Permutations"
    return select(S, len(S))


def n_selections_with_replacement(n, k):
    """
    Number of positive integers solutions to x₁ + x₂ + ⋯ + x_n = n+k
    (Linear diophantine equation)

    Also known as "((n choose k))" with doubled parentheses instead if single.

    https://www.johndcook.com/blog/select_with_replacement/

    """
    return binom(n+k-1, k)


def sumsto(n, k):
    assert n >= 0 and k >= 0
    if k == 0:
        return
    elif k == 1:
        yield (n,)
    else:
        for j in range(n+1):
            for js in sumsto(n-j, k-1):
                yield (j, *js)


# TODO: see itertools.{combinations combinations_with_replacement, permutations,
# product} those implementations are fair because they are based on "pools"

# TODO: implement "fair" versions of all methods (when they exist)

# TODO: implement set-partition enumeration

# TODO: figure out the fair enumerate extension and get all the special cases
# for free.  We know that a fair enumerator exists because the `string` is a
# superset of all other sets.

def sample(S, k, ordered, replace):
    S = tuple(S)

    if k == 0:
        yield ()
    else:
        for i, s in enumerate(S):

            if     ordered and     replace: X = S[:i] + S[i:]    # string
            if     ordered and not replace: X = S[:i] + S[i+1:]  # select
            if not ordered and     replace: X =         S[i:]    # ????
            if not ordered and not replace: X =         S[i+1:]  # choose

            for x in sample(X, k-1, ordered, replace):
                yield (s,) + x


def select(S, k):
    "Ordered subsets of size k"
    return sample(S, k, ordered=True, replace=False)


def choose(S, k):
    "Unordered subsets of size k"
    return sample(S, k, ordered=False, replace=False)


def permute(S):
    "Permutations"
    return select(S, len(S))


def perm_sign(p):
    if len(p) == 1: return True
    t = _inversions(p)
    return -1 if t % 2 else +1


try:
    from blist import sortedlist
except ImportError:
    pass
def _fast_inversions(p):
    n = len(p)
    total = 0
    S = sortedlist()
    for k in reversed(range(n)):
        pos = S.bisect_left(p[k])
        S.add(p[k])
        total += pos
    return total

def _slow_inversions(p):
    n = len(p)
    t = 0
    for i in range(n):
        for j in range(i+1, n):
            if p[i] > p[j]:
                t += 1
    return t

def _inversions(p):
    #assert _slow_inversions(p) == _fast_inversions(p)
    return _fast_inversions(p)


# Note: There is no way to fairly enumerate powerset when S is infinite
def powerset(S):
    "Powerset"
    # choose all subsets of size k from variables
    for k in range(len(S)+1):
        yield from choose(S, k)


# TODO: If we use a dovetailed Cartesian products, then we can support fair
# enumerate over infinite sequences S.
def string(S, k):
    "Strings of length k"
    return sample(S, k, ordered=True, replace=True)


# TODO: if we "parse" left-to-right (instead of top-down) then we can support
# fair enumeration over infinite sequences S.
def trees(S):
    "Generate all binary trees over sequence S."
    S = tuple(S)

    def _trees(i, k):
        if k-i == 1:
            yield S[i]
        else:
            for j in range(i, k):
                for y in _trees(i, j):
                    for z in _trees(j, k):
                        yield (y, z)

    return _trees(0, len(S))


def kleene(S, n=None):
    """
    Kleene closure of S: The set of strings over the alphabet `S` with the option
    to specify a maximum length `n` or leave as `None`.
    """

    def _kleene(n):
        if n is not None and n < 0: return
        yield ()
        for x in _kleene(n if n is None else n-1):
            for s in S:
                yield x + (s,)

    return _kleene(n)


def catalan(n):
    """Catalan numbers:
    `1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900, ...`

    Number of ways to insert balanced parentheses in a sequence of `n+1` symbols.

      - for `n=1` there is 1 way: `(ab)`
      - for `n=2` there are 2 ways: `((ab)c) or (a(bc))`;
      - for `n=3` there are 5 ways: `((ab)(cd)), (((ab)c)d), ((a(bc))d), (a((bc)d)), (a(b(cd)))`.

    References:
    - https://en.wikipedia.org/wiki/Catalan_number
    - https://oeis.org/A000108

    """
    return int(binom(2*n, n)) // (n+1)


def enumerate_digraphs(n):
    "Enumerate all directed graphs over `n` nodes."
    import networkx as nx, numpy as np
    for e in product(*([[0,1]]*(n*n))):
        e = np.array(e).reshape((n, n))
        yield nx.from_numpy_matrix(e, create_using = nx.DiGraph)


# Less efficient version
#def sumsto(n, k):
#    assert n >= 0 and k >= 0
#    for js in product(range(n+1), repeat=k):
#        if sum(js) == n:
#            yield js


def test_sumsto():
    for n in range(8):
        for k in range(n+1):
            #print(f'\nn={n}, k={k}')

            N = 0
            for js in sumsto(n, k):
                N += 1
                #print(' ➥', js)
                assert sum(js) == n
                assert len(js) == k
                assert all(j >= 0 for j in js)

            have = N
            want = binom(n+k-1, n)
            #print('total', colors.mark(have==want), have, want)
            assert have == want


def test_sample():
    print('[sample]')

    def check(N,K):
        S = range(N)
        assert binom(N,K) == length(sample(S, K, ordered=0, replace=0))
        #A01 = sample(S, K, ordered=0, replace=1)   # ???
        assert binom(N,K) * factorial(K) == length(sample(S, K, ordered=1, replace=0))
        assert N**K == length(sample(S, K, ordered=1, replace=1))

    check(5,3)

    # Check corner cases
    check(5,5)
    check(5,0)


def test_kleene():
    print('[kleene]')
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

    assert length(powerset(range(5))) == 2**5
    assert length(permute(range(5))) == factorial(5)


def length(xs):
    return sum(1 for _ in xs)


def flatten(S):
    if not isinstance(S, (list, tuple)):
        yield S
    else:
        for x in S:
            yield from flatten(x)


def test_trees():

    _catalan = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786,
                208012, 742900, 2674440]

    for n in range(1, len(_catalan)):
        assert _catalan[n] == catalan(n), [n, _catalan[n], catalan(n)]

    verbose = False

    def test(S):
        A = list(trees(S))
        if verbose: print(f'\ntrees of {S}')
        for x in A:
            if verbose: print('  ', x)
            # Check that flattening tree gives the seqence `S`.
            assert tuple(flatten(x)) == tuple(S)
        assert length(A) == catalan(n-1)

    for n in range(2, 10):
        print(f'[trees] n={n}' )
        test(range(n))


def segmentations(S):
    "Enumerate all segmentations of S"
    N = len(S)
    p = [[] for _ in range(N+1)]
    p[0] = [()]
    for t in range(1, N+1):
        for s in range(t):
            p[t] += [prefix + (tuple(S[s:t]),) for prefix in p[s]]
    return p[N]


def test_segementations():

    verbose = False

    def test(S):
        A = list(segmentations(S))
        if verbose: print(f'\nsegementations of {S}')
        for i, p in enumerate(sorted(A)):
            if verbose: print(f'  {i}: {p}')
            # Check that `p` is actually a segmentation of S.
            assert ''.join(''.join(s) for s in p) == ''.join(S), S
        # Check that we have the correct number
        assert len(A) == 2 ** (len(S) - 1)
        # Check for duplicates
        assert len(A) == len(set(A))

    for n in range(2, 10):
        print(f'[segmentations] n={n}')
        test(tuple(map(str,range(n))))


#class Collection:
#    def __init__(self, xs):
#        self.xs = list(xs)
#    def __hash__(self):
#        return hash(self.xs)
#    def __repr__(self):
#        return repr(self.xs)
#    def __eq__(self, other):
#        return self.xs == other.xs
#    def choose(self, k):
#        return Collection(choose(self.xs, k))
#    def permute(self):
#        return Collection(permute(self.xs))
#    def select(self, k):
#        return Collection(select(self.xs, k))
#    def strings(self, k):
#        return Collection(sample(self.xs, k, ordered=True, replace=True))
#    def misc(self, k):
#        return Collection(sample(self.xs, k, ordered=False, replace=True))
#

#print(Collection('abcd').choose(3))
#print(Collection('ab').strings(3))
#print(Collection('ab').misc(3))
#print(Collection('abcd').select(3))
#exit()


if __name__ == '__main__':
    from arsenal import testing_framework
    testing_framework(globals())
