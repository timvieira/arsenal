from numpy import searchsorted, cumsum, array
from numpy.random import random

def weighted_choice(p, n):
    """
    Generate n samples of the indicies of the vector of probabilites p
    sampled indicies are placed in an array of length n.
    """
    # uniformly distributed random vector of length n
    y = random((n,))
    # cumulative probability vector
    c = cumsum(p)
    return searchsorted(c, y)

if __name__ == '__main__':

    p = array((0.1, 0.2, 0.6, 0.1)) # vector of probabilities, normalized to 1
    print toss(c, 10)               # generate 10 samples
