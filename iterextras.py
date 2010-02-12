import sys, time

from operator import getitem, sub, mul
from itertools import *
from random import shuffle

# IDEAS:
# * progress_meter: updates based on how much work was dones, e.g.,
#     >> p = progress_meter(100)
#     0.0%
#     >> p.update(10)
#     10.0%

import heapq

def imerge(*iterables):
    '''Merge multiple sorted inputs into a single sorted output.

    Equivalent to:  sorted(itertools.chain(*iterables))

    >>> list(imerge([1,3,5,7], [0,2,4,8], [5,10,15,20], [], [25]))
    [0, 1, 2, 3, 4, 5, 5, 7, 8, 10, 15, 20, 25]

    '''
    heappop, siftup, _StopIteration = heapq.heappop, heapq._siftup, StopIteration

    h = []
    h_append = h.append
    for it in map(iter, iterables):
        try:
            next = it.next
            h_append([next(), next])
        except _StopIteration:
            pass
    heapq.heapify(h)

    while 1:
        try:
            while 1:
                v, next = s = h[0]      # raises IndexError when h is empty
                yield v
                s[0] = next()           # raises StopIteration when exhausted
                siftup(h, 0)            # restore heap condition
        except _StopIteration:
            heappop(h)                  # remove empty iterator
        except IndexError:
            return


##def interleave(*iters):
##    """ take several iterators and weave them together, much like roundrobin does except with different ordering. """

# def iter_partition(it, weights, shuffle=None):
#     """ partition an iterator according to weights, return an len(weights) iterators
#
#     ** Do this in an ONLINE FASHION so that we don't need to know the length of the iterator **
#
#     """
#     if shuffle:
#         it = list(it)
#         random.shuffle(it)
#     it = iter(it)


def floor(stream, baseline=None):
    """Generate the stream of minimum values from the input stream.

    The baseline, if supplied, is an upper limit for the floor.
    >>> ff = floor((1, 2, -2, 3))
    >>> assert list(ff) == [1, 1, -2, -2]
    >>> ff = floor((1, 2, -2, 3), 0)
    >>> assert list(ff) == [0, 0, -2, -2]
    """
    stream = iter(stream)
    m = baseline
    if m is None:
        try:
            m = stream.next()
            yield m
        except StopIteration:
            pass
    for s in stream:
        m = min(m, s)
        yield m

def ceil(stream):
    """Generate the stream of maximum values from the input stream.

    >>> top = ceil([0, -1, 2, -2, 3])
    >>> assert list(top) == [0, 0, 2, 2, 3]
    """
    stream = iter(stream)
    try:
        M = stream.next()
        yield M
    except StopIteration:
        pass
    for s in stream:
        M = max(M, s)
        yield M

def accumulate(stream):
    """Generate partial sums from the stream.

    >>> accu = accumulate([1, 2, 3, 4])
    >>> assert list(accu) == [1, 3, 6, 10]
    """
    total = 0
    for s in stream:
        total += s
        yield total

def diff(s, t):
    """Generate the differences between two streams

    If the streams are of unequal length, the shorter is truncated.
    >>> dd = diff([2, 4, 6, 8], [1, 2, 3])
    >>> assert list(dd) == [1, 2, 3]
    """
    return imap(sub, s, t)

def last(stream, default=None):
    """Return the last item in the stream or the default if the stream is empty.

    >>> last('abc')
    'c'
    >>> last([], default=-1)
    -1
    """
    s = default
    for s in stream:
        pass
    return s


# TODO: can we be lazier? require fewer passes thru X?
def k_fold_cross_validation(X, K, randomize=False):
    """
    Generates K (training, validation) pairs from the items in X.

    Each pair is a partition of X, where validation is an iterable
    of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.

    If randomise is true, a copy of X is shuffled before partitioning,
    otherwise its order is preserved in training and validation.


    >>> for train, test in k_fold_cross_validation(range(3), 3):
    ...     print 'test:', test, ' train:', list(train)
    test: [0]  train: [1, 2]
    test: [1]  train: [0, 2]
    test: [2]  train: [0, 1]

    """
    if randomize:
        X = list(X)
        shuffle(X)

    # folds = [X[i::K] for i in xrange(K)]

    # run thru X once and splitting into folds
    folds = [[] for k in xrange(K)]
    for i, item in enumerate(X):
        folds[i % K].append(item)

    for k in xrange(K):
        training = chain(*(fold for j, fold in enumerate(folds) if j != k))
        yield training, folds[k]


def xCross(sets, *more):
    """
    Take the cartesian product of two or more iterables.
    The input can be either one argument, a collection of iterables xCross([it1,it2,...]),
    or several arguments, each one an iterable xCross(it1, itb, ...).

    >>> [(x,y,z) for x,y,z in xCross([1,2], 'AB', [5])]
    [(1, 'A', 5), (1, 'B', 5), (2, 'A', 5), (2, 'B', 5)]

    """
    if more:
        sets = chain((sets,), more)
    sets = list(sets)
    wheels = map(iter, sets) # wheels like in an odometer
    digits = [it.next() for it in wheels]
    while True:
        yield digits[:]
        for i in range(len(digits)-1, -1, -1):
            try:
                digits[i] = wheels[i].next()
                break
            except StopIteration:
                wheels[i] = iter(sets[i])
                digits[i] = wheels[i].next()
        else:
            break


def cross_product(A,B):
    """ take the cartesian product of two iterables A and B. """
    for a in A:
        for b in B:
            yield (a,b)


def unique_everseen(iterable, key=None):
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


# Recipe credited to George Sakkis
def roundrobin(*iterables):
    """ roundrobin('ABC', 'D', 'EF') --> A D E B F C

    >>> list(roundrobin('ABC', 'D', 'EF'))
    ['A', 'D', 'E', 'B', 'F', 'C']
    """
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def sliding_window(iterable, k):
    """
    s -> (s[0],...,s[k]) (s[1],...,s[k+1]) ... (s[i],...,s[i+k]) ... (s[n-1-k],...,s[n-1])

    >>> [x+y+z for x,y,z in sliding_window('abcdef', 3)]
    ['abc', 'bcd', 'cde', 'def']

    """
    iterators = tee(iterable, k)
    for i, it in enumerate(iterators):
        # advance iterator, 'it',  by i steps
        for j in xrange(i):
            try:
                it.next()    # advance by one
            except StopIteration:
                pass
    return izip(*iterators)


## TODO: add an option for changing the size
def iterview(x, every_k=None):
   """
   iterator which prints its progress to *stderr*.
   """
   WIDTH = 70

   def plainformat(n, lenx):
       return '%5.1f%% (%*d/%d)' % ((float(n)/lenx)*100, len(str(lenx)), n, lenx)

   def bars(size, n, lenx):
       val = int((float(n)*size)/lenx + 0.5)
       if size - val:
           spacing = ">" + (" "*(size-val))[1:]
       else:
           spacing = ""
       return "[%s%s]" % ("="*val, spacing)

   def eta(elapsed, n, lenx):
       if n == 0:
           return '--:--:--'
       if n == lenx:
           secs = int(elapsed)
       else:
           secs = int((elapsed/n) * (lenx-n))
       mins, secs = divmod(secs, 60)
       hrs, mins = divmod(mins, 60)
       return '%02d:%02d:%02d' % (hrs, mins, secs)

   def format(starttime, n, lenx):
       out = plainformat(n, lenx) + ' '
       if n == lenx:
           end = '     '
       else:
           end = ' ETA '
       end += eta(time.time() - starttime, n, lenx)
       out += bars(WIDTH - len(out) - len(end), n, lenx)
       out += end
       return out

   starttime = time.time()
   lenx = len(x)
   for n, y in enumerate(x):
       if every_k is None or n % every_k == 0:
           sys.stderr.write('\r' + format(starttime, n, lenx))
       yield y
   sys.stderr.write('\r' + format(starttime, n+1, lenx) + '\n')


#_______________________________________________________________________________
#

def take(n, seq):
    """ Return the first n items in a sequence. """
    return list(islice(seq, n))

def nth(iterable, n):
    """ Returns a list containing the nth item. """
    return list(islice(iterable, n, n+1))

def no(seq, pred=None):
    """"
    the opposite of all, returns True if pred(x) is false for every element
    in the iterable.
    """
    for elem in ifilter(pred, seq):
        return False
    return True

def quantify(seq, pred=None):
    """ Count how many times the predicate is true in the sequence """
    return sum(imap(pred, seq))

def padnone(seq):
    """ Returns the sequence elements and then returns None indefinitely """
    return chain(seq, repeat(None))

def ncycles(seq, n):
    """ Returns the sequence elements n times """
    return chain(*repeat(seq, n))

def dotproduct(vec1, vec2):
    """ Return the dot product between two vectors. """
    return sum(imap(mul, vec1, vec2))

def flatten(listOfLists):
    """ (non-recursive) Flatten a list of lists. """
    return list(chain(*listOfLists))

# the following are written by dmcc -- not in the real iterextras
def batch(iterable, batchsize=2):
    """Yield a list of (up to) batchsize items at a time.  The last
    element will be shorter if there are items left over.
    batch(s, 2) -> [s0,s1], [s2,s3], [s4, s5], ...


    >>> list(batch(range(5), 2))
    [[0, 1], [2, 3], [4]]

    """
    current = []
    for item in iterable:
        current.append(item)
        if len(current) == batchsize:
            yield current
            current = []
    if current:
        yield current

def full_batches(iterable, batchsize=2):
    """ Differs from batch in that it returns only batchs of size equal to batchsize, no less.

    >>> list(full_batches(range(5), 2))
    [(0, 1), (2, 3)]
    """
    return izip(*repeat(iter(iterable), batchsize))

def batch_extra_lazy(iterable, batchsize):
    """ batch(s, 2) -> [s0,s1], [s2,s3], [s4, s5], ...

    Yield a list of (up to) batchsize items at a time.

    >>> map(tuple, batch_extra_lazy(range(5), 2))
    [(0, 1), (2, 3), (4,)]
    """
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, batchsize)
        yield chain([batchiter.next()], batchiter)


def iunzip(iterable, n=None):
    """Takes an iterator that yields n-tuples and returns n iterators
    which index those tuples.  This function is the reverse of izip().
    n is the length of the n-tuple and will be autodetected if not
    specified.  If the iterable contains tuples of differing sizes,
    the behavior is undefined."""
    # a braindead implementation for now (since it relies on tee() which is
    # braindead in this module (but not in Python 2.4+))
    iterable = iter(iterable) # ensure we're dealing with an iterable
    if n is None: # check the first element for length
        first = iterable.next()
        n = len(first)
        # now put it back in to iterable is unchanged
        iterable = chain([first], iterable)

    iter_tees = tee(iterable, n)
    selector = lambda index: lambda item: getitem(item, index)
    return [imap(selector(i), it) for i,it in izip(count(), iter_tees)]

if __name__ == "__main__":

    a0,b0,c0 = range(1, 10), range(21, 30), range(81, 90)
    test = zip(a0,b0,c0)
    a, b, c = iunzip(test)
    a, b, c = map(list, (a,b,c))
    assert a == a0 and b == b0 and c == c0
    recombined = zip(a, b, c)
    assert recombined == test

    def example_iterview():
        for x in iterview(xrange(400), every_k=20):
            time.sleep(0.01)
    #example_iterview()

    import doctest; doctest.testmod(verbose=True)
