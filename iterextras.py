"""Some useful iterator functions from py2.4 test_itertools.py plus a
couple added items."""

from itertools import *
__all__ = ['take', 'tabulate', 'iteritems', 'nth', 'all', 'any', 'no',
    'quantify', 'padnone', 'ncycles', 'dotproduct', 'flatten',
    'repeatfunc', 'pairwise', 'tee', 'iunzip', 'batch', 'xCross']

#_______________________________________________________________________________
# TIM:

def xCross(sets):
    """ take the cartesian product of a bunch of iterables. """
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

# TODO: maybe add option for padding.
def sliding_window(iterable, k):
    "s -> (s[0],...,s[k]), (s[1],...,s[k+1]), ..., (s[i],...,s[i+k]), (s[n-1-k],...,s[n-1])"
    iterators = tee(iterable, n=k)
    for i, it in enumerate(iterators):
        # advance iterator, 'it',  by i steps
        for j in xrange(i):
            try:
                it.next()    # advance by one
            except StopIteration:
                pass
    return izip(*iterators)


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

def example_iterview():
    print '-----'
    for x in iterview(xrange(1000), every_k=20):
        import time
        time.sleep(0.01)
        print x
    print '---------'

#_______________________________________________________________________________
#

def take(n, seq):
    """Return the first n items in a sequence."""
    return list(islice(seq, n))

def tabulate(function):
    "Return function(0), function(1), ..."
    return imap(function, count())

def iteritems(mapping):
    """Same as dict.iteritems()"""
    return izip(mapping.iterkeys(), mapping.itervalues())

def nth(iterable, n):
    "Returns the nth item"
    return list(islice(iterable, n, n+1))

def all(seq, pred=None):
    "Returns True if pred(x) is true for every element in the iterable"
    for elem in ifilterfalse(pred, seq):
        return False
    return True

def any(seq, pred=None):
    "Returns True if pred(x) is true for at least one element in the iterable"
    for elem in ifilter(pred, seq):
        return True
    return False

def no(seq, pred=None):
    "Returns True if pred(x) is false for every element in the iterable"
    for elem in ifilter(pred, seq):
        return False
    return True

def quantify(seq, pred=None):
    "Count how many times the predicate is true in the sequence"
    return sum(imap(pred, seq))

def padnone(seq):
    "Returns the sequence elements and then returns None indefinitely"
    return chain(seq, repeat(None))

def ncycles(seq, n):
    "Returns the sequence elements n times"
    return chain(*repeat(seq, n))

def dotproduct(vec1, vec2):
    """Return the dot product between two vectors."""
    return sum(imap(operator.mul, vec1, vec2))

def flatten(listOfLists):
    """Flatten a list of lists."""
    return list(chain(*listOfLists))

def repeatfunc(func, times=None, *args):
    "Repeat calls to func with specified arguments."
    "   Example:  repeatfunc(random.random)"
    if times is None:
        return starmap(func, repeat(args))
    else:
        return starmap(func, repeat(args, times))

# attempt to use the real itertools.tee from python2.4
try:
    tee = itertools.tee
except NameError:
    # provide a simple implementation instead
    def tee(iterable, n=2):
        "tee(iterable, n=2) --> tuple of n independent iterators."
        # TODO this is a braindead implementation
        l = list(iterable)
        return [iter(l) for x in range(n)]

# pad option added by dmcc
def pairwise(iterable, pad=False):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    try:
        b.next()
    except StopIteration:
        pass

    if pad:
        return izip(a, padnone(b))
    else:
        return izip(a, b)



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
    return [imap(selector(index), iter_tee) 
        for index, iter_tee in izip(count(), iter_tees)]

if __name__ == "__main__":
    test = zip(range(1, 10), range(21, 30), range(81, 90))
    print test
    a, b, c = iunzip(test)
    al = list(a)
    bl = list(b)
    cl = list(c)
    print al
    print bl
    print cl
    recombined = zip(al, bl, cl)
    assert recombined == test
