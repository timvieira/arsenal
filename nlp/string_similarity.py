from itertools import repeat
from array import array

def LCS(a, b, costfn=lambda a,b: a != b, empty=None, just_length=0):
    """
    Calculate the minimum cost for aligning the elements in the sequence a
    with the elements in the sequence b with respect to costfn.

    usage:
        >>> LCS('121', '212')
        (2.0, [('1', None), ('2', '2'), ('1', '1'), (None, '2')])
    """

    N = len(a)
    M = len(b)
    M1 = M+1

    # allocated some space
    c = array('f')
    c.extend(repeat(0, (N+1)*(M+1)))

    # intialize for all empty matches
    for i in xrange(N):
        c[i*M1+M] = costfn(a[i], empty)+ c[(i+1)*M1+M]

    # intialize for all empty matches
    for j in xrange(M):
        c[N*M1+j] = costfn(empty, b[j])+c[N*M1+(j+1)]

    # fill in table
    for i in reversed(xrange(N)):
        for j in reversed(xrange(M)):
            c[i*M1+j] = min(costfn( a[i],  b[j]) + c[(i+1)*M1 + (j+1)],  # no_gap
                            costfn( a[i], empty) + c[(i+1)*M1 + ( j )],  # insert_gap1
                            costfn(empty,  b[j]) + c[( i )*M1 + (j+1)])  # insert_gap2

    if just_length:
        return c[0]

    # backtrace to find an optimal alignment
    y1s = []
    y2s = []

    i = 0
    j = 0
    while (i < N or j < M):
        c12 = c[i*M1+j]
        if i < N and j < M and c12 == costfn(a[i], b[j]) + c[(i+1)*M1+(j+1)]:
            y1s.append(a[i])
            y2s.append(b[j])
            i += 1
            j += 1
        elif i < N and c12 == costfn(a[i], empty) + c[(i+1)*M1+j]:
            y1s.append(a[i])
            i += 1
            y2s.append(empty)
        else:
            y1s.append(empty)
            y2s.append(b[j])
            j += 1

    return (c[0], zip(y1s, y2s))


def pprint_alignment(A):
    print '\n'.join(map('%18r -> %r'.__mod__, A))


if __name__ == '__main__':

    def test():
        costfn = lambda a,b: 1.5 if (a is None or b is None) else float(a != b)

        cost, _ = LCS('121', '212', costfn=costfn)
        assert cost == 3.0

        a = 'The man saw a small dog with the telescope.'.split()
        b = 'The man saw the smelly dog with the telescope.'.split()
        cost, alignment = LCS(a, b, costfn=costfn)
        assert cost == 2.0
        assert len(alignment) == len(a)

        import doctest
        locals()['pprint_alignment'] = pprint_alignment
        doctest.run_docstring_examples("""
        >>> pprint_alignment(alignment)
                     'The' -> 'The'
                     'man' -> 'man'
                     'saw' -> 'saw'
                       'a' -> 'the'
                   'small' -> 'smelly'
                     'dog' -> 'dog'
                    'with' -> 'with'
                     'the' -> 'the'
              'telescope.' -> 'telescope.'
        """, locals(), verbose=0)

        doctest.testmod()

        print 'passed tests.'

    test()
