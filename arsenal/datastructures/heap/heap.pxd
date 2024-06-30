cdef class Vector:

    cdef public:
        int cap
        int end
        double[:] val

    cpdef int push(self, double x)
    cpdef object pop(self)
    cdef void grow(self)
    cdef void ensure_size(self, int i)
    cdef double get(self, int i)
    cdef void set(self, int i, double v)


cdef class MaxHeap:

    cdef public:
        Vector val

#    def pop(self)
#    def peek(self)
#    def push(self, v)
    cdef void swap(self, int i, int j)
    cdef int up(self, int i)
    cdef int down(self, int i)
    cdef int _update(self, int i, double old, double new)
    cdef void _remove(self, int i)


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

#    def pop(self)
#    def popitem(self)
#    def peek(self)
    cdef void _remove(self, int i)
    cdef _setitem(self, object k, double v)
#    def __delitem__(self, k)
#    def __contains__(self, k)
#    def __getitem__(self, k)
#    def __setitem__(self, k, v)
    cdef void swap(self, int i, int j)
#    def check(self)
#    cdef _update(self, int i, double old, double new)
