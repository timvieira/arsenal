# cython: language_level=3, boundscheck=False, infer_types=True, nonecheck=False
# cython: overflowcheck=False, initializedcheck=False, wraparound=False, cdivision=True
import numpy as np

from libc.stdlib cimport rand
from libc.math cimport log2, ceil
cdef extern from "limits.h":
    int INT_MAX

cdef double MAX = float(INT_MAX)
cdef inline double uniform() nogil:
    return rand() / MAX


cdef class SumHeap:
    cdef readonly:
        double[:] S
        int n, d

    def __init__(self, double[:] w):
        self.n = w.shape[0]
        self.d = int(2**ceil(log2(self.n)))   # number of intermediates
        self.S = np.zeros(2*self.d)           # intermediates + leaves
        self.heapify(w)

    def __getitem__(self, int k):
        return self.S[self.d + k]

    def __setitem__(self, int k, double v):
        self.update(k, v)

    cpdef void heapify(self, double[:] w):
        "Create sumheap from weights `w` in O(n) time."
        d = self.d; n = self.n
        self.S[d:d+n] = w                         # store `w` at leaves.
        for i in reversed(range(1, d)):
            self.S[i] = self.S[2*i] + self.S[2*i + 1]

    cpdef void update(self, int k, double v):
        "Update w[k] = v` in time O(log n)."
        i = self.d + k
        self.S[i] = v
        while i > 0:   # fix parents in the tree.
            i //= 2
            self.S[i] = self.S[2*i] + self.S[2*i + 1]

    cpdef int sample(self, u=None):
        "Sample from sumheap, O(log n) per sample."
        cdef double left, p
        if u is None: u = uniform()
        d = self.S.shape[0]//2     # number of internal nodes.
        p = u * self.S[1]  # random probe, p ~ Uniform(0, z)
        # Use binary search to find the index of the largest CDF (represented as a
        # heap) value that is less than a random probe.
        i = 1
        while i < d:
            # Determine if the value is in the left or right subtree.
            i *= 2            # Point at left child
            left = self.S[i]  # Probability mass under left subtree.
            if p > left:      # Value is in right subtree.
                p -= left     # Subtract mass from left subtree
                i += 1        # Point at right child
        return i - d

    cpdef long[:] swor(self, int k):
        "Sample without replacement `k` times."
        cdef long[:] z = np.zeros(k, dtype=int)
        for i in range(k):
            k = self.sample()
            z[i] = k
            self.update(k, 0)
        return z
