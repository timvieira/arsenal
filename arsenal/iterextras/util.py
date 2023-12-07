import heapq
from operator import getitem, itemgetter
from itertools import chain, count, cycle, islice, repeat, tee
from random import shuffle
from collections import defaultdict
from arsenal.iterview import iterview


class head_iter:
    def __init__(self, iterator):
        self.done = False
        self.head = None
        self.tail = iter(iterator)
        self.__next__()
    def __lt__(self, other):
        return self.head < other.head
    def __next__(self):
        h = self.head
        try:
            self.head = self.tail.__next__()
        except StopIteration:
            self.done = True
            self.head = None
        return h


class buf_iter:
    "Lazy, random access wrapper around an iterator."
    def __init__(self, x):
        self.buf = []
        self.x = iter(x)
        self.j = 0     # num things emitted

    def __iter__(self):
        return self

    def __next__(self):
        try:
            y = self[self.j]
            self.j += 1
            return y
        except IndexError:
            raise StopIteration()

    def __len__(self):
        for _ in self: pass
        return len(self.buf)

    def __getitem__(self, i):
        k = i - len(self.buf)
        while k >= 0:
            try:
                self.buf.append(self.x.__next__())
            except StopIteration:
                raise IndexError(i)
            k -= 1
        return self.buf[i]


def argmax(f, seq):
    """
    >>> argmax(lambda x: -x**2 + 1, range(-10,10))
    0
    """
    return argmax2(f,seq)[1]


def argmax2(f, seq):
    """
    >>> argmax2(lambda x: -x**2 + 1, range(-10,10))
    (1, 0)
    """
    return max(((f(x),x) for x in seq), key=itemgetter(0))


def argmin(f, seq):
    """
    >>> argmin(lambda x: x**2 + 1, range(-10,10))
    0
    """
    return argmin2(f,seq)[1]


def argmin2(f, seq):
    """
    >>> argmin2(lambda x: x**2 + 1, range(-10,10))
    (1, 0)
    """
    return min(((f(x),x) for x in seq), key=itemgetter(0))


def groupby2(s, key=lambda x: x):
    """
    Eager version of groupby which does what you'd expect groupby to do.

    >>> dict(groupby2(range(10), lambda x: x % 2))
    {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}
    """
    groups = defaultdict(list)
    for x in s:
        groups[key(x)].append(x)
    return groups


def atmost(k, seq):
    """
    >>> atmost(1, [0,0,0])
    True

    >>> atmost(1, [0,1,0])
    True

    >>> atmost(1, [0,1,1])
    False
    """
    cnt = 0
    if cnt > k:
        return False
    for x in seq:
        if x:
            cnt += 1
            if cnt > k:
                return False
    return True


def flatten(xs, types=(list, tuple)):
    if isinstance(xs, types):
        for x in xs:
            yield from flatten(x, types)
    else:
        yield xs


def partition(data, proportion):
    """
    Deterministically partition `data` according to proportion.
    Note: assumes sum(proportion) <= 1.0

    >>> partition(range(10), [0.3, 0.7])
    [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]
    """
    assert(sum(proportion) <= 1)
    data = list(data)
    D = iter(data)
    N = len(data)
    return [list(take(j, D)) for j in [int(p*N) for p in proportion]]


def breadth_first(tree, children=iter, depth=-1, queue=None):
    """Traverse the nodes of a tree in breadth-first order.

    - (No need to check for cycles.)

    - The first argument should be the tree root;

    - children should be a function taking as argument a tree node and returning
      an iterator of the node's children.

    """
    if queue is None:
        queue = []
    queue.append(tree)
    while queue:
        node = queue.pop(0)
        yield node
        if depth != 0:
            try:
                queue += children(node)
                depth -= 1
            except (StopIteration, TypeError, IndexError):
                pass


def compress(data, selectors):
    """
    >>> list(compress('ABCDEF', [1,0,1,0,1,1]))
    ['A', 'C', 'E', 'F']
    """
    return (d for d, s in zip(data, selectors) if s)


def k_fold_cross_validation(X, K, randomize=False):
    """
    Generates K (training, validation) pairs from the items in X.

    Each pair is a partition of X, where validation is an iterable
    of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.

    If randomise is true, a copy of X is shuffled before partitioning,
    otherwise its order is preserved in training and validation.


    >>> for train, test in k_fold_cross_validation(range(3), 3):
    ...     print('test:', test, ' train:', list(train), sep=' ')
    test: [0]  train: [1, 2]
    test: [1]  train: [0, 2]
    test: [2]  train: [0, 1]

    """
    if randomize:
        X = list(X)
        shuffle(X)

    # folds = [X[i::K] for i in xrange(K)]

    # run thru X once and splitting into folds
    folds = [[] for k in range(K)]
    for i, item in enumerate(X):
        folds[i % K].append(item)

    for k in range(K):
        training = chain(*(fold for j, fold in enumerate(folds) if j != k))
        yield training, folds[k]


def unique(iterable, key=None):
    """ List unique elements, preserving order. Remember all elements ever seen. """
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in iterable:
            if element not in seen:
                seen_add(element)
                yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def window(iterable, k):
    """
    s -> (s[0],...,s[k]) (s[1],...,s[k+1]) ... (s[i],...,s[i+k]) ... (s[n-1-k],...,s[n-1])

    >>> [x+y+z for x,y,z in window('abcdef', 3)]
    ['abc', 'bcd', 'cde', 'def']

    """
    iterators = tee(iterable, k)
    for i, it in enumerate(iterators):
        # advance iterator, 'it',  by i steps
        for _ in range(i):
            try:
                next(it)    # advance by one
            except StopIteration:
                pass
    return zip(*iterators)


#_______________________________________________________________________________
#

def drop(iterator, n):
    "Advance the iterator n-steps ahead."
    # advance to the emtpy slice starting at position n
    next(islice(iterator, n, n), None)


def take(n, seq):
    """ Return the first n items in a sequence. """
    return islice(seq, None, n)


def padnone(seq):
    """ Returns the sequence elements and then returns None indefinitely """
    return chain(seq, repeat(None))


def ncycles(seq, n):
    """
    Returns the sequence elements n times.
    """
    return chain(*repeat(seq, n))


def batch(size, iterable):
    """Yield a list of (up to) batchsize items at a time.  The last
    element will be shorter if there are items left over.
    batch(s, 2) -> [s0,s1], [s2,s3], [s4, s5], ...

    >>> list(batch(2, range(5)))
    [[0, 1], [2, 3], [4]]
    """
    current = []
    for item in iterable:
        current.append(item)
        if len(current) == size:
            yield current
            current = []
    if current:
        yield current


if __name__ == '__main__':
    import doctest
    doctest.testmod()
