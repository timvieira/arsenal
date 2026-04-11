from bisect import bisect_left


def sorted_intersection(A, B):
    """Baeza-Yates set intersection, aka double-binary search.

    Let `N = min(|A|, |B|)` and `M=max(|A|, |B|)`

     - hash-based set intersection: O(N+M)
     - Baeza-Yates intersection: O(N log M) worst-case, better for most problems
       on "average"

    References:
    - https://mail.python.org/pipermail/python-list/2008-April/508321.html

    """

    if len(A) > len(B): A,B = B,A   # The smaller set drives the outer loop.

    def rec(lo1, hi1, lo2, hi2):
        if hi1 <= lo1: return
        if hi2 <= lo2: return

        mid1 = (lo1 + hi1) // 2
        x1 = A[mid1]                                # median of this part of set A

        mid2 = bisect_left(B, x1, lo=lo2, hi=hi2)   # find position of mid1 in B

        yield from rec(lo1, mid1, lo2, mid2)     # recurse on the first halves

        # Is the median of `A` in the intersection? (uses binary search above)
        if mid2 < hi2 and x1 == B[mid2]:
            #assert max(A[lo1], B[lo2]) <= x1 <= min(A[hi1-1], B[hi2-1])
            yield x1     # recursing in this order ensures that `out` is sorted.

        yield from rec(mid1+1, hi1, mid2, hi2)   # recurse on the second halves

    yield from rec(0, len(A), 0, len(B))

