from itertools import repeat
from array import array

def LCS(x1s, x2s, costfn, just_length=0):
    """
    calculate the minimum cost for aligning the elements in the sequence x1s
    with the elements in the sequence x2s with respect to costfn.

    usage:

        1) Define a token edit distance function AND an empty token.
           For example:

               def token_dist(s1,s2):        
                   if s1 == s2:
                       return 0
                   elif s1 == token_dist.empty and s2 != token_dist.empty: # GAP penalty
                       return 1.25
                   elif s1 != token_dist.empty and s2 == token_dist.empty: # GAP penalty
                       return 1.25
                   else:
                       return 1        # you can make this the levenstein distance

               token_dist.empty = None

        2) Tokenize strings: by default a string can be iterated and indexed, but
           often, this is not the desired tokenization. You can call LCS with any iterable
           of strings.

        3) Call LCS:

               a = '121'
               b = '212'
               print LCS(a, b, token_dist)
               print

               a = 'The man saw small dog with the telescope.'.split()
               b = 'The man saw smelly dog with the telescope.'.split()
               print LCS(a, b, token_dist)
    
    """

    n1 = len(x1s)
    n2 = len(x2s)
    n21 = n2+1

    # allocated some space
    c = array('f')
    c.extend(repeat(0, (n1+1)*(n2+1)))

    # intialize for all empty matches
    for i1 in reversed(xrange(n1)):
        c[i1*n21+n2] = costfn(x1s[i1], costfn.empty)+ c[(i1+1)*n21+n2]

    # intialize for all empty matches
    for i2 in reversed(xrange(n2)):
        c[n1*n21+i2] = costfn(costfn.empty, x2s[i2])+c[n1*n21+(i2+1)]

    # fill in table
    for i1 in reversed(xrange(n1)):
        for i2 in reversed(xrange(n2)):
            # ** remember you're working backwards in the table **

            no_gap      = costfn(x1s[i1], x2s[i2])      + c[(i1+1)*n21 + (i2+1)]
            insert_gap1 = costfn(x1s[i1], costfn.empty) + c[(i1+1)*n21 + ( i2 )]
            insert_gap2 = costfn(costfn.empty, x2s[i2]) + c[( i1 )*n21 + (i2+1)]

            c[i1*n21+i2] = min(no_gap, insert_gap1, insert_gap2)
            

    if just_length:
        return c[0]

    # backtrace to find an optimal alignment
    y1s = []
    y2s = []
    
    i1 = 0
    i2 = 0
    while (i1 < n1 or i2 < n2):
        c12 = c[i1*n21+i2]
        if i1 < n1 and i2 < n2 and c12 == costfn(x1s[i1], x2s[i2]) + c[(i1+1)*n21+(i2+1)]:
            y1s.append(x1s[i1])
            y2s.append(x2s[i2])
            i1 += 1
            i2 += 1
        elif i1 < n1 and c12 == costfn(x1s[i1], costfn.empty) + c[(i1+1)*n21+i2]:
            y1s.append(x1s[i1])
            i1 += 1
            y2s.append(costfn.empty)
        else:
            y1s.append(costfn.empty)
            y2s.append(x2s[i2])
            i2 += 1

    return (c[0], zip(y1s, y2s))


def pprint_alignment(A):
    print '\n'.join(map('%s -> %s'.__mod__, A))


if __name__ == '__main__':

    def token_dist(s1,s2):        
        if s1 == s2:
            return 0
        elif s1 == token_dist.empty and s2 != token_dist.empty: # GAP penalty
            return 1.25
        elif s1 != token_dist.empty and s2 == token_dist.empty: # GAP penalty
            return 1.25
        else:
            return 1        # you can make this the levenstein distance

    token_dist.empty = None

    a = '121'
    b = '212'
    print LCS(a, b, token_dist)
    print

    a = 'The man saw a small dog with the telescope.'
    b = 'The man saw the smelly dog with the telescope.'
    print LCS(a.split(), b.split(), token_dist)





