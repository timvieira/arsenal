import numpy as np
import pylab as pl
from numpy import array, exp, log, dot, abs, multiply, cumsum, arange, \
    asarray, ones, mean, searchsorted, sqrt, isfinite
from numpy.random import uniform, normal
from scipy.linalg import norm as _norm
from scipy import stats
from arsenal.terminal import colors
from arsenal.iterview import progress
from scipy.stats import pearsonr, spearmanr
from contextlib import contextmanager
from scipy.special import expit as sigmoid
from scipy.linalg import svd


def wide_dataframe():
    import pandas as pd
    from arsenal.terminal import console_width
    pd.set_option('display.width', console_width())


@contextmanager
def set_printoptions(*args, **kw):
    "Context manager for numpy's print options."
    was = np.get_printoptions()
    np.set_printoptions(*args, **kw)
    yield
    np.set_printoptions(**was)


def argmin_random_tie(x):
    "argmin with randomized tie breaking."
    return np.random.choice(np.flatnonzero(x == x.min()))


def argmax_random_tie(x):
    "argmax with randomized tie breaking."
    return np.random.choice(np.flatnonzero(x == x.max()))


def onehot(i, n):
    """Create a one-hot vector: a vector of length `n` with a `1` at position `i`
    and zeros elsewhere.

    """
    x = np.zeros(n)
    x[i] = 1
    return x


def null_space(A, eps=1e-15):
    "Find V such that AVx = 0 for all x."
    _, s, Vh = svd(A)
    s2 = np.zeros(Vh.shape[0])
    s2[0:len(s)] = s
    mask = s2 < eps
    null = Vh[mask,:]
    return null.T


def wls(A, b, w):
    "weighted least-squares estimation."
    from statsmodels.api import WLS
    # Note: statsmodel is a bit more accurate than directly calling lstsq
    return WLS(b, A, weights=w).fit().params


def split_ix(N, p, randomize=1):
    "Sample a random partition of N integers with proportions `p`."
    if randomize:
        I = np.random.permutation(N)
    else:
        I = list(range(N))
    folds = []
    for q in p:
        j = int(np.ceil(N*q))
        fold = I[:j]
        folds.append(fold)
        I = I[j:]
    return folds


def norm(x, p=2):
    if not isfinite(x).all():
        return np.nan
    return _norm(x, p)


def zero_retrieval(expect, got):
    "How good are we at retrieving zero values? Measured with F1 score."
    assert expect.shape == got.shape
    # F1 on zeros
    A = (expect == 0)
    B = (got == 0)
    C = (A & B).sum()
    A = A.sum()
    B = B.sum()
    R = C / A if A != 0 else 1.0
    P = C / B if B != 0 else 1.0
    F = 2*P*R/(P+R) if (P+R) != 0 else 1.0
    return F


def relative_difference(a, b):
    """Element-wise relative difference of two arrays

    Definition:
      { 0                          if if x=y=0
      { abs(x-y) / max(|x|, |y|)   otherwise

    Choices for denominator include:

      max(|x|, |y|)  # problem with x=y=0

      avg(x, y)      # problem with x = -y; gives geometric mean

      avg(|x|, |y|)  # problem when x=y=0

    Further reading:
      http://en.wikipedia.org/wiki/Relative_change_and_difference

    """

    a = array(a).flatten()
    b = array(b).flatten()
    #x = np.atleast_2d(array([a, b]))
    #fs = abs(x).max(axis=0)
    #fs[fs == 0] = 1
    #return (abs(x[0,:] - x[1,:]) / fs).flatten()

    es = []
    for x,y in zip(a,b):
        if x == y:  # covers inf, but not nan
            e = 0
        else:
            s = max(abs(x), abs(y))
            if s == 0:
                s = 1
            e = abs(x-y) / s
        es.append(e)
    return np.array(es)



def linf(a, b):
    return abs(a - b).max()


# Notes: I'm not using `scipy.spatial.distance.cosine` because it doesn't handle
# the zero norm cases.
def cosine(a, b):
    if not isfinite(a).all() or not isfinite(b).all():
        return np.nan
    A = norm(a)
    B = norm(b)
    if A == 0 and B == 0:
        return 1.0
    elif A != 0 and B != 0:
        return a.dot(b) / (A*B)
    else:
        return np.nan


def is_distribution(p):
    p = asarray(p)
    return (p >= 0).all() and abs(1 - p.sum()) < 1e-10


class Mixture(object):
    """
    Mixture of several densities
    """
    def __init__(self, w, pdfs):
        w = array(w)
        assert is_distribution(w), \
            'w is not a prob. distribution.'
        self.pdfs = pdfs
        self.w = w
        self.cdf = cumsum(w)

    def rvs(self, size=1):
        # sample component
        i = self.cdf.searchsorted(uniform(size=size))
        # sample from component
        return array([self.pdfs[j].rvs() for j in i])

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

    x = array(a, copy=True)
    x.sort()

    def f(z):
        return searchsorted(x, z, 'right') * 1.0 / len(x)

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
    a = w - w.max()
    exp(a, out=a)
    return sample(a)


def cumavg(x):
    """
    Cumulative average.

    >>> cumavg([1,2,3,4,5])
    array([ 1. ,  1.5,  2. ,  2.5,  3. ])

    """
    return cumsum(x) / arange(1.0, len(x)+1)


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
    rescale = data.ptp(axis=0)
    #rescale[rescale == 0] = 1.0  # avoid divide by zero
    x = (data - shift)
    x /= rescale
    return x


def mean_confidence_interval(a, confidence=0.95):
    "returns (mean, lower, upper)"
    a = asarray(a)
    n = a.shape[0]
    m = mean(a)
    h = a.std(ddof=1) / sqrt(n) * stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h


def normalize(x, p=1):
    return x / norm(x, p)


def lidstone(p, delta):
    """
    Lidstone smoothing is a generalization of Laplace smoothing.
    """
    return normalize(p + delta)


# based on implementation from scikits-learn
def logsumexp(arr, axis=None):
    """Computes the sum of arr assuming arr is in the log domain.

    Returns log(sum(exp(arr))) while minimizing the possibility of
    over/underflow.

    Examples
    --------

    >>> a = arange(10)
    >>> log(sum(exp(a)))
    9.4586297444267107
    >>> logsumexp(a)
    9.4586297444267107

    >>> x = [[0, 0, 1000.0], [1000.0, 0, 0]]
    >>> logsumexp(x, axis=1)
    array([ 1000.,  1000.])

    >>> logsumexp(x)
    1000.6931471805599

    >>> logsumexp(x, axis=0)
    array([  1.00000000e+03,   6.93147181e-01,   1.00000000e+03])

    """
    arr = np.array(arr, dtype=np.double)
    if axis is None:
        arr = arr.ravel()
    else:
        arr = np.rollaxis(arr, axis)
    # Use the max to normalize, as with the log this is what accumulates the
    # less errors
    vmax = arr.max(axis=0)
    arr -= vmax
    exp(arr, out=arr)
    out = log(arr.sum(axis=0))
    out += vmax
    return out


def softmax(x, axis=None):
    """
    >>> x = [1, -10, 100, .5]
    >>> softmax(x)
    array([  1.01122149e-43,   1.68891188e-48,   1.00000000e+00,
             6.13336839e-44])
    >>> exp(x) / exp(x).sum()
    array([  1.01122149e-43,   1.68891188e-48,   1.00000000e+00,
             6.13336839e-44])

    >>> x = [[0, 0, 1000], [1000, 0, 0]]

    Normalize by row:
    >>> softmax(x, axis=0)
    array([[ 0. ,  0.5,  1. ],
           [ 1. ,  0.5,  0. ]])

    Normalize by column:
    >>> softmax(x, axis=1)
    array([[ 0.,  0.,  1.],
           [ 1.,  0.,  0.]])

    Normalize by cell:
    >>> softmax(x, axis=None)
    array([[ 0. ,  0. ,  0.5],
           [ 0.5,  0. ,  0. ]])

    """
    a = np.array(x, dtype=np.double)
    if axis is None:
        v = a.ravel()
    else:
        v = np.rollaxis(a, axis)
    v -= v.max(axis=0)
    exp(v, out=v)
    v /= v.sum(axis=0)
    return a


from arsenal.misc import deprecated
@deprecated('softmax')
def exp_normalize(arr, axis=None):
    return softmax(arr, axis=axis)


# TODO: add support for the axis argument.
def d_softmax(out, x, adj):
    """
    out = softmax(x), adj are the adjoints we're chain-ruling together.
    """
    g = adj - adj.dot(out)
    g *= out
    return g


# TODO: implement projection onto l1 ball -- see code in notes.
def project_onto_simplex(a, radius=1.0):
    """
    Project point a to the probability simplex.
    Returns (the projected point x, the zero threshold, and the residual value).

    """
    a = np.array(a)
    x0 = a.copy()
    d = len(x0)
    ind_sort = np.argsort(-x0)
    y0 = x0[ind_sort]
    ycum = np.cumsum(y0)
    val = 1.0/np.arange(1,d+1) * (ycum - radius)
    ind = np.nonzero(y0 > val)[0]
    rho = ind[-1]
    tau = val[rho]
    y = y0 - tau
    ind = np.nonzero(y < 0)
    y[ind] = 0
    x = x0.copy()
    x[ind_sort] = y
    return x, tau, .5*np.dot(x-a, x-a)



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
    nz = p.nonzero()
    p = p[nz]
    q = q[nz]
    return p.dot(log(p) - log(q)) / log_of_2
#    return dot(p, log(p) - log(q)) / log_of_2


# KL(p||q) = sum_i p[i] log(p[i] / q[i])
#          = sum_i p[i] (log p[i] - log q[i])
#          = sum_i p[i] log p[i] - sum_i p[i] log(q[i])
#          = Entropy(p) + CrossEntropy(p,q)

def mutual_information(joint):
    """
    Mutual Information

    MI(x,y) = KL( p(x,y) || p(x) p(y) )

    We can compute this easily from the joint distribution

      joint = p(X=x,Y=y)

    because
      p(X=x) = sum_y p(X=x, Y=y)
      p(Y=y) = sum_x p(X=x, Y=y)

    relationships:
      MI(x,y) is the expected PMI(x,y) wrt p(x,y)
      MI(x,y) = KL(p(x,y) || p(x) p(y))

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


def assert_equal(a, b, name='', verbose=False, throw=True, tol=1e-10, color=1):
    """isfinite: asserts that *both* `a` and `b` must be finite.

    >>> assert_equal(0, 1, throw=0, color=0)
    0 1 err=1 fail

    >>> assert_equal(0, 0, verbose=1, color=0)
    0 0 err=0 ok

    """
    try:
        assert not np.isnan(a).any() and not np.isnan(b).any()
    except (TypeError, AssertionError):
        msg = '%sexpected %s, got %s' % ('%s: ' % name if name else '',
                                         a, b)
        if throw:
            raise AssertionError(msg)
        else:
            print(msg)

    err = inf_norm(a,b)
    if np.array(a == b).all():   # handles the non-finite cases.
        err = 0
    if name:
        name = '%s: ' % name
    if verbose or err > tol:
        msg = '%s%g %g err=%g' % (name, a, b, err)
        if throw and err > tol:
            raise AssertionError(msg + ' >= tolerance (%s)' % tol)
        else:
            if not color:
                print(msg, 'ok' if err < tol else 'fail', sep=' ')
            else:
                print(msg, colors.green % 'ok' if err < tol else colors.red % 'fail', sep=' ')


if __name__ == '__main__':
    #import doctest; doctest.testmod()

    def run_tests():

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

        def test_softmax_grad():
            from arsenal.maths.checkgrad import fdcheck
            n = 20
            adj = np.random.uniform(-1,1,size=n)
            x = np.random.uniform(-1,1,size=n)
            out = softmax(x)
            g = d_softmax(out, x, adj)
            fdcheck(lambda: softmax(x).dot(adj), x, g)

        test_softmax_grad()

        assert relative_difference(np.inf, np.inf) == 0.0

        print('passed tests.')

    run_tests()
