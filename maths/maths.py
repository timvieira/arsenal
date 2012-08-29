from __future__ import division
from numpy import array, empty, zeros
import math
from math import exp as math_exp, log as math_log
from operator import itemgetter

from misc import deprecated

INF = float('infinity')
NEG_INF = float('-infinity')

'''
from math import sqrt

def naive_hypot(x,y):
    return sqrt(x*x + y*y)

@deprecated("numpy.hypot")
def robust_hypot(x,y):
    """
    Compute sqrt(x*x + y*y) without risking overflow.

    Lets pick a pick number:
      >>> big = 1e300
      >>> big            # still representable
      1e300
      >>> big*big        # but not "squarable"
      inf

    Obviously, naive `hypot` can't handle this one:
      >>> hypot(1e300, 1.0e300)
      inf

    But what about `robust_hypot`:
      >>> c = robust_hypot(big, big)
      >>> c
      1.4142135623730952e+300
      >>> c == big*sqrt(2)    # 2*b*b == c*2  =>  c = sqrt(2)*b
      True

    Success!
    """
    M = max(abs(x), abs(y))
    m = min(abs(x), abs(y))
    r = m / M
    return M*sqrt(1 + r*r)
'''

def exp(x):
    try:
        return math_exp(x)
    except OverflowError:
        return INF

# should use scipy.maxentropy.robustlog
def log(x):
    if x < 1e-10:
        return 0.0
    else:
        return math_log(x)

def argmax(f, seq):
    """
    >>> argmax(lambda x: -x**2 + 1, range(-10,10))
    0
    """
    return argmax2(f,seq)[1]

def argmax2(f, seq):
    """
    >>> argmax2(lambda x: -x**2 + 1, range(-10,10))
    (1, 0)
    """
    return max(((f(x),x) for x in seq), key=itemgetter(0))

def argmin(f, seq):
    return argmin2(f,seq)[1]

def argmin2(f, seq):
    return min(((f(x),x) for x in seq), key=itemgetter(0))


log_of_2 = math.log(2)

def entropy(p):
    """Calculate entropy of a discrete random variable with given probabilities."""
    return -sum(pi*log(pi) for pi in p if pi > 0) / log_of_2

def kl_divergence(p, q):
    """ Compute KL divergence of two vectors, K(p || q).
    NOTE: If any value in q is 0.0 then the KL-divergence is infinite.
    """
    assert len(p) == len(q)
    kl = sum(p[i] * log(p[i] / q[i]) for i in xrange(len(p)) if p[i] != 0.0)
    return kl / log_of_2

def jensen_shannon_divergence(p, q):
    """ Returns the Jensen-Shannon divergence. """
    assert len(p) == len(q)
    average = zeros(len(p))
    for i in xrange(len(p)):
        average[i] += (p[i] + q[i]) / 2.0
    return (kl_divergence(p, average) + kl_divergence(q, average)) / 2.0

def normalize(x):
    """ Divide each element of the array by the sum of the elements. """
    return (1.0/sum(x)) * array(x)

def normalize_inplace(x):
    """ Divide each element of the array by the sum of the elements IN PLACE. """
    if isinstance(x,dict):
        Z = sum(x.itervalues())
        for k in x:
            x[k] /= Z
    else:
        Z = sum(x)
        for i in xrange(len(x)):
            x[i] /= Z

def exp_normalize(A):
    """
    Exponentiate elements of the array, and then normalize them to sum to one.

    exp(xi) / (exp(x1) + ... + exp(xn))
         = exp(xi-B)*exp(B) / (exp(B)*(exp(x1-B) + ... + exp(xn-B)))  for any B
         = exp(xi-B) / (exp(x1-B) + ... + exp(xn-B))                  for any B
    """
    M = max(A)
    B = empty(len(A))
    for k in xrange(len(A)):
        B[k] = exp(A[k] - M)
    Z = sum(B)
    for k in xrange(len(A)):
        B[k] /= Z
    return B

def exp_normalize_inplace(A):
    """ Exponentiate the elements of the array, and then normalize them to sum to one. """
    if isinstance(A,dict):
        M = max(A.itervalues())
        for k in A:
            A[k] = exp(A[k] - M)
        Z = sum(A.itervalues())
        for k in A:
            A[k] /= Z
    else:
        M = max(A)
        for k in xrange(len(A)):
            A[k] = exp(A[k] - M)
        Z = sum(A)
        for k in xrange(len(A)):
            A[k] /= Z

def normalize_log_prob(a):
    # normalizeLogProb: [log(a), log(b), log(c)] --> [log(a/Z), log(b/Z), log(c/Z)] where Z = a+b+c
    # expNormalize: [log(a), log(b), log(c)] --> [a/Z, b/Z, c/Z] where Z=a+b+c
    b = exp_normalize(a)
    for i in xrange(len(b)):
        b[i] = log(b[i])
    return b

def normalize_log_prob_inplace(a):
    exp_normalize_inplace(a)
    for i in xrange(len(a)):
        a[i] = log(a[i])

def logsumexp(x):
    """
    The log-sum-exp trick:
      log(sum(exp(xi) for xi in X)) <=> log(sum(exp(xi-B) for xi in X)) + B   for any B

    picking B = max(X), can help prevent problems with numerical overflow.
    """
    B = max(x)
    return log(sum(exp(x-B) for x in x if x > NEG_INF)) + B

def sum_two_log_probs(a, b):
    """
    Returns the sum of two doubles expressed in log space
       sumLogProb = log (e^a + e^b)
                  = log e^a(1 + e^(b-a))
                  = a + log (1 + e^(b-a))

    By exponentiating (b-a), we obtain better numerical precision than
    we would if we calculated e^a or e^b directly.
    """
    if b < a:
        return a + log(1 + exp(b-a))
    else:
        return b + log(1 + exp(a-b))

def subtract_log_prob(a, b):
    """ Returns the difference of two doubles expressed in log space """
    if b < a:
        return a + log(1 - exp(b-a))
    else:
        return b + log(1 - exp(a-b))

def sum_log_prob(vals):
    """
    Sums an array of numbers [log(x1), ..., log(xn)] returns log(x1+x2+...+xn)

    This saves some of unnecessary calls to log in the two-argument version.

    usage:
        >>> x = [0.7, 0.1, 0.2]
        >>> abs(sum_log_prob(map(log, x)) - log(sum(x))) < 1e-7
        True

    NOTE: this implementation IGNORES elements of the input array that are more
    than LOGTOLERANCE (currently 30.0) less than the maximum element.

    CREDIT: this function has been adapted from Stanford NLP package, SloppyMath.java
    """
    LOGTOLERANCE = 30.0
    N = len(vals)
    M = -INF
    maxidx = 0
    for i in xrange(N):
        if vals[i] > M:
            M = vals[i]
            maxidx = i
    anyAdded = False
    intermediate = 0.0
    cutoff = M - LOGTOLERANCE
    for i in xrange(maxidx):
        if vals[i] >= cutoff:
            anyAdded = True
            intermediate += exp(vals[i] - M)
    for i in xrange(maxidx + 1, N):
        if vals[i] >= cutoff:
            anyAdded = True
            intermediate += exp(vals[i] - M)
    return M + log(1.0 + intermediate) if anyAdded else M


if __name__ == '__main__':
    import doctest; doctest.testmod()

    assert entropy((0.5, 0.5)) == 1.0
    assert abs(entropy((0.75, 0.25)) - 0.8112781244) < 1e-10
    assert abs(entropy((0.1, 0.1, 0.8)) == 0.9219280948) < 1e-10
