class BucketQueue:
    """BucketQueue.py
    Taken from https://github.com/timvieira/dyna-pi/blob/main/dyna/util/bucket_queue.py

    A simple priority queue with integer priorities. Use like:
        Q = BucketQueue()
        Q[item] = priority
        del Q[item]
        for item in Q: ...

    The time to find and return each item in the queue is proportional
    to the difference (current priority - previous priority), or O(1) if
    this difference is non-positive. In particular when the minimum priority
    is non-negative and non-decreasing (as in Dijkstra's algorithm) or when
    its decreases are bounded (as in graph degeneracy) the total time for a
    sequence of operations is proportional to the number of operations plus
    the maximum priority.

    D. Eppstein, July 2016.

    References:
    * https://www.ics.uci.edu/~eppstein/261/s21w5.pdf

    """
    def __init__(self):
        """Create a new empty integer priority queue."""
        self._D = {}        # map from items to priorities
        self._Q = {}        # map from priorities to buckets
        self._N = None      # lower bound on min priority

    def __getitem__(self, item):
        "Look up the priority of an item."
        return self._D[item]

    def __delitem__(self, item):
        "Remove an item from the priority queue."
        priority = self._D[item]
        del self._D[item]               # remove from map of items => priorities
        self._Q[priority].remove(item)  # remove from bucket
        if not self._Q[priority]:
            del self._Q[priority]       # remove empty bucket

    def __setitem__(self, item, priority):
        "Add an element to the priority queue with the given priority."
        if not isinstance(priority, int):
            raise TypeError("Priority must be an integer")
        if item in self._D:
            del self[item]
        self._D[item] = priority        # add to map of items => priorities
        if not self._Q or priority < self._N:
            self._N = priority          # update priority lower bound
        if priority not in self._Q:
            self._Q[priority] = set()   # make new bucket if necessary
        self._Q[priority].add(item)     # and add to bucket

    def __iter__(self):
        """Repeatedly find and remove the min-priority item from the queue.
        It is ok for the queue to be modified between iterations."""
        while self._Q:
            while self._N not in self._Q:
                self._N += 1
            x = next(iter(self._Q[self._N]))    # arbitrary item in 1st bucket
            del self[x]
            yield x

    def popitem(self):
        while self._Q:
            while self._N not in self._Q:
                self._N += 1
            x = next(iter(self._Q[self._N]))    # arbitrary item in 1st bucket
            del self[x]
            return (x, self._N)

    def pop(self):
        while self._Q:
            while self._N not in self._Q:
                self._N += 1
            x = next(iter(self._Q[self._N]))    # arbitrary item in 1st bucket
            del self[x]
            return x

    def items(self):
        """Variant iterator that generates (item,priority) pairs.
        We rely on the fact that the usual __iter__ always
        leaves self._N equal to the priority."""
        for x in self:
            yield (x, self._N)

    def __contains__(self, item):
        "Container class membership test."
        return item in self._D

    def __len__(self):
        "Container class length."
        return len(self._D)
