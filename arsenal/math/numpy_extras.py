from __future__ import division
import numpy as np
from numpy import array, exp, log, dot, abs, multiply, cumsum
from numpy.random import uniform, normal
from scipy.linalg import norm
from numpy import isfinite


def compare(expect, got, name=None):
    """
    Compare vectors.
    """
    from arsenal.terminal import yellow, green, red
    assert len(expect) == len(got)

    errors = []
    if not isfinite(got).all():
        errors.append('not finite')

    if not isfinite(expect).all():
        errors.append('not finite')

    c = 1-cosine(expect, got)
    if c > 1e-10:
        errors.append('cosine dist: %g' % c)

    d = linf(expect, got)
    if d > 1e-10:
        errors.append('l_inf: %g' % d)

    x = expect
    y = got
    s = np.asarray(~((x > 0) ^ (y > 0)), dtype=int)
    p = s.sum() * 100.0 / len(s)
    if p != 100.0:
        errors.append('same sign: %s%% (%s/%s)' % (p, s.sum(), len(s)))
        errors.append('same sign vec: %s' % s)

    if errors:
        print
        print red % 'Failed%s:' % ' (%s)' % name if name else ''
        print yellow % 'expected:'
        print expect
        print yellow % 'got:'
        print got
        print yellow % 'errors:'
        print '\n'.join(errors)
    else:
        print green % 'ok%s' \
            % ' (%s)' % name if name else ''


def linf(a, b):
    return abs(a - b).max()


def cosine(a, b):
    return a.dot(b) / norm(a) / norm(b)


class Mixture(object):
    """
    Mixture of several densities
    """
    def __init__(self, w, pdfs):
        w = array(w)
        assert (w >= 0).all() and abs(1 - w.sum()) <= 1e-10, \
            'w is not a prob. distribution.'
        self.pdfs = pdfs
        self.w = w
        self.cdf = np.cumsum(w)

    def rvs(self):
        # sample component
        i = self.cdf.searchsorted(uniform())
        # sample from component
        return self.pdfs[i].rvs()

    def pdf(self, x):
        return sum([p.pdf(x) * w for w, p in zip(self.w, self.pdfs)])


def spherical(size):
    "Generate random vector from spherical Gaussian."
    x = normal(0, 1, size=size)
    x /= norm(x, 2)
    return x


def cdf(a):
    """
    Empirical CDF of data `a`, returns function which makes values to their
    cumulative probabilities.

     >>> g = cdf([5, 10, 15])

    Evaluate the CDF at a few points

     >>> g([5,9,13,15,100])
     array([ 0.33333333,  0.33333333,  0.66666667,  1.        ,  1.        ])


    Check that ties are handled correctly

     >>> g = cdf([5, 5, 15])

     The value p(x <= 5) = 2/3

     >>> g([0, 5, 15])
     array([ 0.        ,  0.66666667,  1.        ])

    """

    x = np.array(a, copy=True)
    x.sort()

    def f(z):
        return np.searchsorted(x, z, 'right') * 1.0 / len(x)

    return f


def sample(w, n=None):
    """
    Uses the inverse CDF method to return samples drawn from an (unnormalized)
    discrete distribution.
    """
    c = cumsum(w)
    r = uniform() if n is None else uniform(size=n)
    return c.searchsorted(r * c[-1])


def log_sample(w):
    "Sample from unnormalized log-distribution."
    return sample(exp(w - w.max()))


def cumavg(x):
    """
    Cumulative average.

    >>> cumavg([1,2,3,4,5])
    array([ 1. ,  1.5,  2. ,  2.5,  3. ])

    """
    return np.cumsum(x) / np.arange(1.0, len(x)+1)


def normalize_zscore(data):
    """
    Shift and rescale data to be zero-mean and unit-variance along axis 0.
    """
    shift = data.mean(axis=0)
    rescale = data.std(axis=0)
    rescale[rescale == 0] = 1.0   # avoid divide by zero
    return (data - shift) / rescale


def normalize_interval(data):
    """
    Shift and rescale data so that it lies in the range [0,1].
    """
    shift = data.min(axis=0)
    rescale = data.max(axis=0) - shift
    rescale[rescale == 0] = 1.0  # avoid divide by zero
    return (data - shift) / rescale


def normalize(p):
    return p / p.sum()


def lidstone(p, delta):
    """
    Lidstone smoothing is a generalization of Laplace smoothing.
    """
    return normalize(p + delta)


# based on implementation from scikits-learn
def logsumexp(arr, axis=0):
    """Computes the sum of arr assuming arr is in the log domain.

    Returns log(sum(exp(arr))) while minimizing the possibility of
    over/underflow.

    Examples
    --------

    >>> a = np.arange(10)
    >>> log(sum(exp(a)))
    9.4586297444267107
    >>> logsumexp(a)
    9.4586297444267107
    """
    arr = np.asarray(arr)
    arr = np.rollaxis(arr, axis)
    # Use the max to normalize, as with the log this is what accumulates the
    # less errors
    vmax = arr.max(axis=0)
    out = log(exp(arr - vmax).sum(axis=0))
    out += vmax
    return out


def exp_normalize(x, T=1.0):
    """
    >>> x = [1, -10, 100, .5]
    >>> exp_normalize(x)
    array([  1.01122149e-43,   1.68891188e-48,   1.00000000e+00,
             6.13336839e-44])
    >>> exp(x) / exp(x).sum()
    array([  1.01122149e-43,   1.68891188e-48,   1.00000000e+00,
             6.13336839e-44])
    """
    y = array(x)      # creates copy
    y /= T
    y -= y.max()
    y = exp(y)
    y /= y.sum()
    return y


log_of_2 = log(2)

def entropy(p):
    "Entropy of a discrete random variable with distribution `p`"
    assert len(p.shape) == 1
    p = p[p.nonzero()]
    return -dot(p, log(p)) / log_of_2


def kl_divergence(p, q):
    """ Compute KL divergence of two vectors, K(p || q).
    NOTE: If any value in q is 0.0 then the KL-divergence is infinite.
    """
    return dot(p, log(p) - log(q)) / log_of_2


# KL(p||q) = sum_i p[i] log(p[i] / q[i])
#          = sum_i p[i] (log p[i] - log q[i])
#          = sum_i p[i] log p[i] - sum_i p[i] log(q[i])
#          = Entropy(p) + CrossEntropy(p,q)

# timv: do we need to specify all three things?
#
#  P(x) = sum_y P(x,y) by law of total probabilty
def mutual_information(joint):
    """
    Mutual Information

    MI(x,y) = KL( p(x,y) || p(x) p(y) )

    joint = p(x,y)
    p = p(x)
    q = q(y)

    relationships:
      MI(x,y) is the expected PMI(x,y) wrt p(x,y)
      MI(x,y) = KL( p(x,y) || p(x) p(y) )

    properties:
      MI(X,Y) = MI(Y,X) is symmetric
    """
    # we can compute px and py from joint by applying the law of total probability
    px = joint.sum(axis=1)
    py = joint.sum(axis=0)
    independent = multiply.outer(px, py)
    assert joint.shape == independent.shape
    return kl_divergence(array(joint.flat), array(independent.flat))


def cross_entropy(p, q):
    """ Cross Entropy of two vectors,

    CE(p,q) = - \sum_i p[i] log q[i]

    Relationship to KL-divergence:

      CE(p,q) = entropy(p) + KL(p||q)
    """
    assert len(p) == len(q)
    p = p[p > 0]
    return -dot(p, log(q)) / log_of_2


def assert_isdistr(p):
    assert (p >= 0).all()
    assert (p <= 1).all()
    assert abs(p.sum() - 1.0) < 0.000001


def equal(a, b, tol=1e-10):
    "L_{\inf}(a - b) < tol"
    return inf_norm(a,b) < tol


def inf_norm(a, b):
    return abs(a - b).max()


def assert_equal(a, b, tol=1e-10):
    err = inf_norm(a,b)
    assert err < tol, 'error = %s >= tolerance (%s)' % (err, tol)


if __name__ == '__main__':
    #import doctest; doctest.testmod()

    def tests():

        # Entropy tests
        assert entropy(array((0.5, 0.5))) == 1.0
        assert abs(entropy(array((0.75, 0.25))) - 0.8112781244) < 1e-10
        assert abs(entropy(array((0.1, 0.1, 0.8))) - 0.9219280948) < 1e-10

        # KL-divergence tests
        assert kl_divergence(array((0.5, 0.5)), array((0.5, 0.5))) == 0.0

        # KL, Entropy, and Cross Entropy relationship
        p = array([0.5, 0.5])
        q = array([0.4, 0.6])
        assert_equal(cross_entropy(p, q), (entropy(p) + kl_divergence(p, q)))

        # Normalize tests
        assert_equal(array([0.5, 0.5]), normalize(array([2, 2])))

        # Mutual Information tests
        #Pjoint = array([[0.25, 0.25], [0.25, 0.25]])

        Pjoint = normalize(np.random.rand(4,10))
        assert_equal(mutual_information(Pjoint),
                     mutual_information(Pjoint.T))

        def mi_independent_is_zero(px, py):
            assert_equal(mutual_information(multiply.outer(px, py)), 0.0)

        mi_independent_is_zero(p, q)
        mi_independent_is_zero(array([0.1, 0.1, 0.2, 0.6]),   # non-square joint
                               array([0.9, 0.1]))


        print 'passed tests.'

    tests()
