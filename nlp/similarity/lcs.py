from numpy import zeros

def default_cost(a,b):
    if a == b:
        return 0.0
    elif a is None or b is None:
        return 1.0
    else:
        return 1000.0

def lcs(a, b, cost=default_cost):

    N = len(a)
    M = len(b)

    c = zeros((N + 1, M + 1))

    for i in reversed(xrange(N)):
        c[i, M] = cost(a[i], None) + c[i + 1, M]

    for j in reversed(xrange(M)):
        c[N, j] = cost(None, b[j]) + c[N, j + 1]

    for i in reversed(xrange(N)):
        for j in reversed(xrange(M)):
            c[i, j] = min(cost(a[i], b[j]) + c[i + 1, j + 1],
                          cost(a[i], None) + c[i + 1, j],
                          cost(None, b[j]) + c[i, j + 1])

    y = []; i = 0; j = 0
    while i < N or j < M:
        cij = c[i, j]
        if i < N and j < M and cij == cost(a[i], b[j]) + c[i + 1, j + 1]:
            y.append((a[i], b[j]))
            i += 1
            j += 1
        elif i < N and cij == cost(a[i], None) + c[i + 1, j]:
            y.append((a[i], None))
            i += 1
        else:
            assert j < M and cij == cost(None, b[j]) + c[i, j + 1]
            y.append((None, b[j]))
            j += 1

    assert i == N and j == M

    return (c[0,0], y)


def longest_increasing_subsequence(a, verbose=False):

    s = a[:]
    s.sort()

    (cost, alignment) = lcs(a, s)

    if verbose:
        print
        print "input:  ", a
        print "sorted: ", s

        print 'cost:', cost
        print
        for (a,b) in alignment:
            print '  %16s => %s' % (a,b)
        print

    return [a for (a,b) in alignment if a is not None and b is not None]


if __name__ == '__main__':
    assert lcs('abc', '') == (3.0, [('a', None), ('b', None), ('c', None)])
    assert lcs('', 'abc') == (3.0, [(None, 'a'), (None, 'b'), (None, 'c')])
    assert lcs('abc', 'abc') == (0.0, [('a', 'a'), ('b', 'b'), ('c', 'c')])
    assert lcs('abcd', 'obce') == (4.0, [('a', None),
                                         (None, 'o'),
                                         ('b', 'b'),
                                         ('c', 'c'), 
                                         ('d', None),
                                         (None, 'e')])
    assert longest_increasing_subsequence([1, 10, 2, 2, 3, -1, 4, -5]) == [1, 2, 2, 3, 4]
    assert longest_increasing_subsequence([20, 1, 2, 2, 3, -1, 4]) == [1, 2, 2, 3, 4]
    
    print 'passed tests.'
