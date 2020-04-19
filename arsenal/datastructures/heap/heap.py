"""
Heap data structures with optional
 - Locators
 - Top-k (Bounded heap)

"""
import numpy as np

Vt = object


class Vector:

    def __init__(self, cap):
        self.cap = cap
        self.val = np.zeros(self.cap, dtype=Vt)
        self.end = 0

    def push(self, x):
        i = self.end
        self.ensure_size(i)
        self.val[i] = x
        self.end += 1
        return i

    def pop(self):
        "pop from the end"
        assert self.end > 0
        self.end -= 1
        v = self.val[self.end]
        self.val[self.end] = np.nan
        return v

    def grow(self):
        self.cap *= 2
        new = np.empty(self.cap, dtype=Vt)
        new[:self.end] = self.val[:self.end]
        self.val = new
        return new

    def ensure_size(self, i):
        "grow in needed"
        if i + 1 > self.val.shape[0]: self.grow()
        return i

    def __getitem__(self, i):
        assert i < self.end
        return self.val[i]

    def __setitem__(self, i, v):
        assert i < self.end
        self.val[i] = v

    def __len__(self):
        return self.end

    def __repr__(self):
        return repr(self.val[:self.end])


class MaxHeap:

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
        return self.val[1]

    def push(self, v):
        # put new element last and bubble up
        return self.up(self.val.push(v))

    def swap(self, i, j):
        assert i < self.val.end
        assert j < self.val.end
        self.val[i], self.val[j] = self.val[j], self.val[i]

    def up(self, i):
        while i > 1:
            p = i // 2
            if self.val[p] >= self.val[i]:
                break
            self.swap(i, p)
            i = p
        return i

    def down(self, i):
        n = self.val.end
        while 2*i < n:
            a = 2 * i
            b = 2 * i + 1
            c = i
            if self.val[a] > self.val[c]:
                c = a
            if b < n and self.val[b] > self.val[c]:
                c = b
            if c == i:
                break
            self.swap(i, c)
            i = c
        return i

    def _update(self, i, old, new):
        assert i < self.val.end
        if old == new: return i   # value unchanged
        self.val[i] = new         # perform change
        if old < new:             # increased
            return self.up(i)
        else:                     # decreased
            return self.down(i)

    def _remove(self, i):
        # update the locator stuff for last -> i
        last = self.val.end - 1
        self.swap(i, last)
        old = self.val.pop()
        # special handling for when the heap has size one.
        if i == last: return
        self._update(i, old, self.val[i])

    def check(self):
        # heap property
        for i in range(2, self.val.end):
            assert self.val[i // 2] >= self.val[i], (self.val[i // 2], self.val[i])   # parent >= child
