from itertools import *

# IDEAS:
# * progress_meter: updates based on how much work was dones, e.g.,
#     >> p = progress_meter(100)
#     0.0%
#     >> p.update(10)
#     10.0%

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

def roundrobin(*iterables):
    """ roundrobin('ABC', 'D', 'EF') --> A D E B F C """
    # Recipe credited to George Sakkis
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
   import time
   import sys
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
    return sum(imap(operator.mul, vec1, vec2))

def flatten(listOfLists):
    """ (non-recursive) Flatten a list of lists. """
    return list(chain(*listOfLists))

# the following are written by dmcc -- not in the real iterextras
def batch(iterable, batchsize=2):
    """Yield a list of (up to) batchsize items at a time.  The last
    element will be shorter if there are items left over.
    batch(s, 2) -> [s0,s1], [s2,s3], [s4, s5], ..."""
    current = []
    for item in iterable:
        current.append(item)
        if len(current) == batchsize:
            yield current
            current = []
    if current:
        yield current

import operator
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
    selector = lambda index: lambda item: operator.getitem(item, index)
    return [imap(selector(i), it) for i,it in izip(count(), iter_tees)]

if __name__ == "__main__":

    a0,b0,c0 = range(1, 10), range(21, 30), range(81, 90)
    test = zip(a0,b0,c0)
    a, b, c = iunzip(test)
    a, b, c = map(list, (a,b,c))
    assert a == a0 and b == b0 and c == c0
    recombined = zip(a, b, c)
    assert recombined == test

    import time
    def example_iterview():
        for x in iterview(xrange(400), every_k=20):
            time.sleep(0.01)
    #example_iterview()

    import doctest; doctest.testmod(verbose=True)
