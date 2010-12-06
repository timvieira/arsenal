
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in xrange(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in xrange(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]


def damerau_levenshtein(a, b):
    """Calculate the Damerau-Levenshtein distance between sequences.

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first sequence into the
    second. Although generally used with strings, any sequences of
    comparable objects will work.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.
    """

    # Conceptually, this is based on a len(a) + 1 * len(b) + 1 matrix.
    # However, only the current and two previous rows are needed at once,
    # so we only store those.
    oneago = None
    thisrow = range(1, len(b) + 1) + [0]
    for x in xrange(len(a)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(b) + [x + 1]
        for y in xrange(len(b)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + float(a[x] != b[y])
            thisrow[y] = min(delcost, addcost, subcost)

            # This block deals with transpositions
            if x > 0 and y > 0:
                if a[x] == b[y-1] and a[x-1] == b[y] and a[x] != b[y]:
                    thisrow[y] = min(thisrow[y], twoago[y-2] + 1)

    return thisrow[len(b) - 1]



