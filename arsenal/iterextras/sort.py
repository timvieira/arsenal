from arsenal.iterextras import buf_iter, head_iter
from heapq import heapify, heappop, _siftup, heappush


def sorted_union(*iterators):
    """
    Merge multiple sorted inputs into a single sorted output.

    Equivalent to `sorted(itertools.chain(*iterables))`, but more efficient and lazy.

    >>> list(merge_sorted([1,3,5,7], [0,2,4,8], [5,10,15,20], [], [25]))
    [0, 1, 2, 3, 4, 5, 5, 7, 8, 10, 15, 20, 25]

    """

    h = [head_iter(s) for s in iterators]
    h = [s for s in h if not s.done]
    heapify(h)
    while h:
        s = h[0]
        yield s.__next__()       # advance the top iterator
        if s.done:
            heappop(h)           # remove empty iterator
        else:
            _siftup(h, 0)        # restore heap condition

merge_sorted = sorted_union


class Item:
    def __init__(self, cost, index, elems):
        self.cost = cost
        self.index = index
        self.elems = elems
    def __lt__(self, other):
        return self.cost < other.cost


# Note: If the product operation is associative, it is best to pick an
# association order rather than use the k-fold product.  It will speed up the
# computation by a factor of k: the k-fold products in the inner loop below
# don't cost O(k) because the effective k is equal to 2.
def sorted_product(p, *iters):
    """
    Sorted product of `iters`, where the output is sorted by a monotonic product
    operator `p`.  Examples: tuples, or multiplication/addition of positive numbers.
    """

    n = len(iters)
    assert n > 1

    # use buffered iterator to ensure (random) access to the previously emitted
    # values of each iterator.
    iters = [buf_iter(it) for it in iters]

    def vals(z):
        return tuple(it[j] for it, j in zip(iters, z))

    # elements in the heap are wrapped `Item` to make it a min heap.
    q = []
    y = (0,)*n

    try:
        heappush(q, Item(p(vals(y)), 0, y))
    except IndexError:
        return   # empty

    while q:
        item = heappop(q)
        x = item.elems
        j = item.index

        yield item.cost

        # next best item must differ by one, enqueue all such items
        # We reduce the number of pushes by the dotted rule trick.
        for i in range(j, n):

            y = list(x)
            y[i] = x[i] + 1
            y = tuple(y)

            #if x[i] + 1 >= len(a[i]): continue
            try:
                iters[i][y[i]]
            except IndexError:
                # `IndexError` is thrown when `iter[i]` is finite and we
                # requested more iterates than it has.
                continue

            heappush(q, Item(p(vals(y)), i, y))

