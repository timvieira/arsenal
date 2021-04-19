# cython: language_level=3, boundscheck=False, infer_types=True, nonecheck=False
# cython: overflowcheck=False, initializedcheck=False, wraparound=False, cdivision=True

"""
Heap data structures with optional
 - Locators
 - Top-k (Bounded heap)

"""
import numpy as np

Vt = np.double
cdef double NaN = np.nan

# TODO: Use the C++ standard library's implementation of a vector of doubles.
cdef class Vector:

    cdef public:
        int cap
        int end
        double[:] val

    def __init__(self, cap):
        self.cap = cap
        self.val = np.zeros(self.cap, dtype=Vt)
        self.end = 0

    cpdef int push(self, double x):
        i = self.end
        self.ensure_size(i)
        self.val[i] = x
        self.end += 1
        return i

    cpdef object pop(self):
        "pop from the end"
        assert 0 < self.end
        self.end -= 1
        v = self.val[self.end]
        self.val[self.end] = NaN
        return v

    cdef void grow(self):
        self.cap *= 2
        new = np.empty(self.cap, dtype=Vt)
        new[:self.end] = self.val[:self.end]
        self.val = new

    cdef void ensure_size(self, int i):
        "grow in needed"
        if self.val.shape[0] < i + 1: self.grow()

    def __getitem__(self, int i):
        assert i < self.end
        return self.get(i)

    cdef double get(self, int i):
        return self.val[i]

    def __setitem__(self, int i, double v):
        assert i < self.end
        self.set(i, v)

    cdef void set(self, int i, double v):
        self.val[i] = v

    def __len__(self):
        return self.end

    def __repr__(self):
        return repr(self.val[:self.end])


cdef class MaxHeap:

    cdef public:
        Vector val

    def __init__(self, cap=2**8):
        self.val = Vector(cap)
        self.val.push(np.nan)

    def __len__(self):
        return len(self.val) - 1   # subtract one for dummy root element

    def pop(self):
        v = self.peek()
        self._remove(1)
        return v

    def peek(self):
        return self.val.val[1]

    def push(self, v):
        # put new element last and bubble up
        return self.up(self.val.push(v))

    cdef void swap(self, int i, int j):
        assert i < self.val.end
        assert j < self.val.end
        self.val.val[i], self.val.val[j] = self.val.val[j], self.val.val[i]

    cdef int up(self, int i):
        while 1 < i:
            p = i // 2
            if self.val.val[p] < self.val.val[i]:
                self.swap(i, p)
                i = p
            else:
                break
        return i

    cdef int down(self, int i):
        n = self.val.end
        while 2*i < n:
            a = 2 * i
            b = 2 * i + 1
            c = i
            if self.val.val[c] < self.val.val[a]:
                c = a
            if b < n and self.val.val[c] < self.val.val[b]:
                c = b
            if c == i:
                break
            self.swap(i, c)
            i = c
        return i

    def _update(self, int i, double old, double new):
        assert i < self.val.end
        if old == new: return i   # value unchanged
        self.val.val[i] = new         # perform change
        if old < new:             # increased
            return self.up(i)
        else:                     # decreased
            return self.down(i)

    def _remove(self, int i):
        # update the locator stuff for last -> i
        last = self.val.end - 1
        self.swap(i, last)
        old = self.val.pop()
        # special handling for when the heap has size one.
        if i == last: return
        self._update(i, old, self.val.val[i])

    def check(self):
        # heap property
        for i in range(2, self.val.end):
            assert self.val[i] <= self.val[i // 2], (self.val[i // 2], self.val[i])   # child <= parent


cdef class LocatorMaxHeap(MaxHeap):
    """
    Dynamic heap. Maintains max of a map, via incrementally maintained partial
    aggregation tree. Also known a priority queue with 'locators'.

    This data structure efficiently maintains maximum of the priorities of a set
    of keys. Priorites may increase or decrease. (Many max-heap implementations
    only allow increasing priority.)

    """

    cdef public:
        dict key
        dict loc

    def __init__(self, **kw):
        super().__init__(**kw)
        self.key = {}   # map from index `i` to `key`
        self.loc = {}   # map from `key` to index in `val`

    def __repr__(self):
        return repr({k: self[k] for k in self.loc})

    def pop(self):
        k,v = self.peek()
        super().pop()
        return k,v

    def popitem(self):
        return self.pop()

    def peek(self):
        return self.key[1], super().peek()

    def _remove(self, int i):
        # update the locator stuff for last -> i
        last = self.val.end - 1
        self.swap(i, last)
        old = self.val.pop()
        # remove the key/loc/val associated with the deleted node.
        self.loc.pop(self.key.pop(last))
        # special handling for when the heap has size one.
        if i == last: return
        self._update(i, old, self.val.val[i])

    def __delitem__(self, k):
        self._remove(self.loc[k])

    def __contains__(self, k):
        return k in self.loc

    def __getitem__(self, k):
        return self.val.val[self.loc[k]]

    def __setitem__(self, k, v):
        "upsert (update or insert) value associated with key."
        cdef int i
        if k in self:
            # update
            i = self.loc[k]
            super()._update(i, self.val[i], v)
        else:
            # insert (put new element last and bubble up)
            i = self.val.push(v)
            # Annoyingly, we have to write key/loc here the super class's push
            # method doesn't allow us to intervene before the up call.
            self.val[i] = v
            self.loc[k] = i
            self.key[i] = k
            # fix invariants
            self.up(i)

    cdef void swap(self, int i, int j):
        assert i < self.val.end
        assert j < self.val.end
        self.val.val[i], self.val.val[j] = self.val.val[j], self.val.val[i]

        self.key[i], self.key[j] = self.key[j], self.key[i]
        self.loc[self.key[i]] = i
        self.loc[self.key[j]] = j

    def check(self):
        super().check()
        for key in self.loc:
            assert self.key[self.loc[key]] == key
        for i in range(1, self.val.end):
            assert self.loc[self.key[i]] == i


class MinMaxHeap:

    def __init__(self, **kw):
        self.max = LocatorMaxHeap(**kw)
        self.min = LocatorMaxHeap(**kw)   # will pass negative values here

    def __contains__(self, k):
        return k in self.max

    def __setitem__(self, k, v):
        self.max[k] = v
        self.min[k] = -v

    def peekmin(self):
        k, v = self.min.peek()
        return k, -v

    def peekmax(self):
        return self.max.peek()

    def popmax(self):
        k, v = self.max.pop()
        self.min._remove(self.min.loc[k])  # remove it from the min heap
        return k, v

    def popmin(self):
        k, v = self.min.pop()
        self.max._remove(self.max.loc[k])  # remove it from the min heap
        return k, -v

    def check(self):
        self.min.check()
        self.max.check()

    def __len__(self):
        return len(self.max)

    def __repr__(self):
        return repr(self.max)

    def map(self):
        return {k: self.max[k] for k in self.max.loc}


class BoundedMaxHeap(MinMaxHeap):

    def __init__(self, maxsize, **kw):
        super().__init__(**kw)
        self.maxsize = maxsize

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        if len(self) > self.maxsize:
            if v < self.peekmin()[1]:  # smaller than the smallest element.
                return
            else:
                self.popmin()   # evict the smallest element

    def pop(self):
        return self.popmax()

    def check(self):
        super().check()
        assert len(self.max) <= self.maxsize
        assert len(self.min) <= self.maxsize
