from itertools import product
from scipy.special import binom, factorial

# TODO: I'm not crazy about this design because the return type should be a
# FiniteSet too.  However, for practical purposes, I want the results to be lazy
# -- since I often use these combinatorial routines to do model checking.
class FiniteSet:

    def __init__(self, Σ):
        self.Σ = tuple(Σ)

    def __iter__(self):
        return iter(self.Σ)

    def __len__(self):
        return len(self.Σ)

    def __getitem__(self, x):
        return FiniteSet(self.Σ.__getitem__(x))

    def __add__(self, x):
        return FiniteSet(self.Σ + x.Σ)

    def __pow__(self, k):
        "Strings of (exactly) length k."
        yield from self.sample(k, ordered=True, replace=True)

    def sample(self, k, ordered, replace):
        if k == 0:
            yield ()
        else:
            for i, σ in enumerate(self):

                if ordered     and not replace: X = self[:i] + self[i+1:]  # select
                if not ordered and not replace: X = self[i+1:]             # choose
                if ordered     and     replace: X = self                   # self**k
                if not ordered and     replace: X = self[i:]               # ????

                for c in X.sample(k-1, ordered, replace):
                    yield c + (σ,)

    def kleene(self, n=None):
        """
        Kleene closure of Σ: The set of strings over the alphabet Σ with the option
        to specify a maximum length `n` or leave as `None`.
        """
        if n is not None and n < 0: return
        yield ()
        for s in self.kleene(n if n is None else n-1):
            for σ in self:
                yield s + (σ,)

    def select(self, k):
        "Ordered subsets of size k"
        yield from self.sample(k, ordered=True, replace=False)

    def choose(self, k):
        "Unordered subsets of size k"
        yield from self.sample(k, ordered=False, replace=False)

    def permutations(self):
        "Permutations"
        return self.select(len(self))

    def powerset(self):
        # choose all subsets of size k from variables
        for k in range(len(self)+1):
            yield from self.choose(k)


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


def permutations(s):
    return FiniteSet(s).permutations()

def choose(s, k):
    return FiniteSet(s).choose(k)

def select(s, k):
    return FiniteSet(s).select(k)

def powerset(s):
    return FiniteSet(s).powerset()



def tests():

    def check(N,K):
        S = FiniteSet(range(N))

        A00 = list(S.sample(K, ordered=0, replace=0))
        assert binom(N,K) == len(A00)

        #A01 = S.sample(K, ordered=0, replace=1)   # ???

        A10 = list(S.sample(K, ordered=1, replace=0))
        assert binom(N,K) * factorial(K) == len(A10)

        A11 = list(S.sample(K, ordered=1, replace=1))
        assert N**K == len(A11)

    check(5,3)

    # Check corner cases
    check(5,5)
    check(5,0)


    from arsenal.iterextras import take

    assert (list(take(10, map(''.join, FiniteSet('01').kleene())))
            == ['', '0', '1', '00', '01', '10', '11', '000', '001', '010'])

    assert (list(map(''.join, FiniteSet('01').kleene(n=3)))
            == ['', '0', '1', '00', '01', '10', '11', '000', '001', '010', '011', '100', '101', '110', '111'])

    assert (list(map(''.join, FiniteSet('a').kleene(n=4)))
            == ['', 'a', 'aa', 'aaa', 'aaaa'])

    assert (list(map(''.join, FiniteSet('').kleene(n=4)))
            == [''])


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    tests()
