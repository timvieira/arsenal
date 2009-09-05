def k_subsets_i(n, k):
    """ Yield each subset of size k from the set of integers 0 .. n - 1 """
    # check base cases
    if k == 0 or n < k:
        yield []
    elif n == k:
        yield range(n) 
    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n - 1, k - 1) + choose(n - 1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.append(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s

def k_subsets(s, k):
    """ Yield all subsets of size k from s """
    s = list(s)
    n = len(s)
    for k_set in k_subsets_i(n, k):
        yield [s[i] for i in k_set]

def powerset(S):
    # number of variables
    n = len(S)
    # choose all subsets of size k from variables
    for k in range(0,n+1):
        for s in k_subsets(S, k):
            yield list(s)

# __________________________________________________________________________
"""
xpermutations.py
Generators for calculating
a) the permutations of a sequence and
b) the combinations and selections of a number of elements from a sequence.
"""

def xcombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in xcombinations(items[:i]+items[i+1:],n-1):
                yield [items[i]]+cc

def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc
            
def xselections(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for ss in xselections(items, n-1):
                yield [items[i]]+ss

def xpermutations(items):
    return xcombinations(items, len(items))

if __name__=="__main__":
    print "Permutations of 'love'"
    for p in xpermutations(['l','o','v','e']): print ''.join(p)

    print
    print "Combinations of 2 letters from 'love'"
    for c in xcombinations(['l','o','v','e'],2): print ''.join(c)

    print
    print "Unique Combinations of 2 letters from 'love'"
    for uc in xuniqueCombinations(['l','o','v','e'],2): print ''.join(uc)

    print
    print "Selections of 2 letters from 'love'"
    for s in xselections(['l','o','v','e'],2): print ''.join(s)

    print
    print map(''.join, list(xpermutations('done')))
