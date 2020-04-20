from heapq import heapify, heappush, heappop


from arsenal.misc import deprecated

class prioritydict(dict):
    """Dictionary that can be used as a priority queue.

    Keys of the dictionary are items to be put into the queue, and values
    are their respective priorities. All dictionary methods work as expected.
    The advantage over a standard heapq-based priority queue is
    that priorities of items can be efficiently updated (amortized O(1))
    using code as 'thedict[item] = new_priority.'

    The 'smallest' method can be used to return the object with lowest
    priority, and 'pop_smallest' also removes it.

    The 'sorted_iter' method provides a destructive sorted iterator.

    This implemented is based on:

      Matteo Dell'Amico's implementation
      http://code.activestate.com/recipes/522995-priority-dict-a-priority-queue-with-updatable-prio/

         which is based on David Eppstein's implementation
         http://code.activestate.com/recipes/117228/

    """

    @deprecated('use arsenal.datastructures.heap.locator')
    def __init__(self, *args, **kwargs):
        super(prioritydict, self).__init__(*args, **kwargs)
        self._heap = None
        self._rebuild_heap()

    def _rebuild_heap(self):
        self._heap = [(v, k) for k, v in self.items()]
        heapify(self._heap)

    def pop_smallest(self, value=False):
        """
        Return the item with the lowest priority and remove it.

        Raises IndexError if the object is empty.
        """

        # Implementation note: Since we don't eagerly remove an element when
        # it's priority changes, we need to filter our pops to make sure the
        # priority isn't stale.

        heap = self._heap
        v, k = heappop(heap)
        while k not in self or self[k] != v:   # while `k` is stale
            v, k = heappop(heap)
        del self[k]
        if value:
            return k, v
        return k


# TODO: this isn't right because we're lazy about cleanup heappop pop_smallest
# calls pop multiple times.
#    def __len__(self):
#        return len(self._heap)

    def __setitem__(self, key, val):
        # We are not going to remove the previous value from the heap, since
        # this would have a cost O(n).
        super(prioritydict, self).__setitem__(key, val)

        if len(self._heap) < 2 * len(self):
            heappush(self._heap, (val, key))
        else:
            # When the heap grows larger than 2 * len(self), we rebuild it from
            # scratch to avoid wasting too much memory.
            self._rebuild_heap()

    setdefault = None
    update = None
