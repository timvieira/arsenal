from itertools import product
from scipy.special import binom, factorial

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

            if     ordered and not replace: X = S[:i] + S[i+1:]  # select
            if not ordered and not replace: X =         S[i+1:]  # choose
            if     ordered and     replace: X = S[:i] + S[i:]    # string
            if not ordered and     replace: X =         S[i:]    # ????

            for x in sample(X, k-1, ordered, replace):
                yield x + (s,)


def select(S, k):
    "Ordered subsets of size k"
    return sample(S, k, ordered=True, replace=False)


def choose(S, k):
    "Unordered subsets of size k"
    return sample(S, k, ordered=False, replace=False)


def permute(S):
    "Permutations"
    return select(S, len(S))


# Note: There is no way to fairly enumerate powerset when S is infinite
def powerset(S):
    "Powerset"
    # choose all subsets of size k from variables
    for k in range(len(S)+1):
        yield from choose(S, k)


# TODO: If use a dovetailed Cartesian products, then we can support fair
# enumerate over infinite sequences S
def string(S, k):
    "Strings of length k"
    return sample(S, k, ordered=True, replace=True)


# TODO: if we "parse" left-to-right (instead of top-down) then we can support
# fair enumeration over infinite sequences S.
def trees(S):
    "Generate all balanced trees over sequence S."
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
    return int(binom(2*n, n)) // (n+1)


def enumerate_digraphs(n):
    "Enumerate all directed graphs over `n` nodes."
    import networkx as nx, numpy as np
    for e in product(*([[0,1]]*(n*n))):
        e = np.array(e).reshape((n, n))
        yield nx.from_numpy_matrix(e, create_using = nx.DiGraph)


#def slow_enumerate_dtrees(n):
#    for G in enumerate_digraphs(n):
#        if nx.is_tree(G):
#            [s,*_] = nx.topological_sort(G)  # get root.
#            if s == 0:
#                yield G



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


def length(x):
    return len(list(x))


def flatten(S):
    if not isinstance(S, (list, tuple)):
        yield S
    else:
        for x in S:
            yield from flatten(x)


#def xCross(sets, *more):
#    """
#    Take the cartesian product of two or more iterables.
#    The input can be either one argument, a collection of iterables xCross([it1,it2,...]),
#    or several arguments, each one an iterable xCross(it1, itb, ...).
#
#    >>> [(x,y,z) for x,y,z in xCross([1,2], 'AB', [5])]
#    [(1, 'A', 5), (1, 'B', 5), (2, 'A', 5), (2, 'B', 5)]
#
#    """
#    if more:
#        sets = chain((sets,), more)
#    sets = list(sets)
#    wheels = map(iter, sets) # wheels like in an odometer
#    digits = [it.next() for it in wheels]
#    while True:
#        yield digits[:]
#        for i in range(len(digits)-1, -1, -1):
#            try:
#                digits[i] = wheels[i].next()
#                break
#            except StopIteration:
#                wheels[i] = iter(sets[i])
#                digits[i] = wheels[i].next()
#        else:
#            break


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


if __name__ == '__main__':
    test_kleene()
    test_sample()
    test_trees()
    test_segementations()
