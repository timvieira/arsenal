from itertools import product

def k_subsets_i(n, k):
    "Subset of size k from the set of integers 0..n-1"
    # check base cases
    if k == 0 or n < k:
        yield []
    elif n == k:
        yield list(range(n))
    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n-1, k-1) + choose(n-1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.append(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s


def k_subsets(s, k):
    "Subsets of size k from s."
    s = list(s)
    n = len(s)
    for k_set in k_subsets_i(n, k):
        yield [s[i] for i in k_set]


def powerset(S):
    n = len(S)
    # choose all subsets of size k from variables
    for k in range(n+1):
        for s in k_subsets(S, k):
            yield list(s)


def combinations(items, n):
    "Ordered combinations"
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in combinations(items[:i]+items[i+1:],n-1):
                yield [items[i]]+cc


def unordered_combinations(items, n):
    "Unordered combinations"
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in unordered_combinations(items[i+1:],n-1):
                yield [items[i]]+cc


def selections(items, n):
    "Combinations with replacement"
    if n==0: yield []
    else:
        for i in range(len(items)):
            for ss in selections(items, n-1):
                yield [items[i]]+ss


def permutations(items):
    "Permutations"
    return combinations(items, len(items))


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


if __name__ == '__main__':

    def test():
        from scipy.special import factorial, binom
        A = list(permutations(['l','o','v','e']))
        assert(len(A) == factorial(4))

        A = list(combinations(['l','o','v','e'], 2))
        assert(len(A) == 2*binom(4, 2))

        A = list(unordered_combinations(['l','o','v','e'], 2))
        assert(len(A) == binom(4, 2))

        A = list(selections(['l','o','v','e'], 2))
        assert(len(A) == 4*4)

        A = list(powerset(['l','o','v','e']))
        assert(len(A) == 2**4)

    test()
