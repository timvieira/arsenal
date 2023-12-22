import random
import numpy as np
from numpy import array, exp, log, dot, abs, multiply, cumsum, arange, \
    asarray, ones, mean, searchsorted, sqrt, isfinite, log1p, expm1
import scipy.linalg as la
from scipy import stats
from arsenal import colors
from scipy.stats import pearsonr, spearmanr
from contextlib import contextmanager
from scipy.special import expit as sigmoid


def wide_dataframe():
    import pandas as pd
    from arsenal import console_width
    pd.set_option('display.width', console_width())


@contextmanager
def set_printoptions(*args, **kw):
    "Context manager for numpy's print options."
    was = np.get_printoptions()
    np.set_printoptions(*args, **kw)
    yield
    np.set_printoptions(**was)


@contextmanager
def restore_random_state(seed=None):
    py_rng = random.getstate()
    np_rng = np.random.get_state()
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    yield (py_rng, np_rng)
    random.setstate(py_rng)
    assert np.random.set_state(np_rng) is None


def fit_curve(xs, ys):
    import matplotlib.pyplot as pl
    xs = np.array(xs); ys = np.array(ys)
    assert np.all(xs > 0) and np.all(ys > 0)
    a,b = np.polyfit(np.log(xs), np.log(ys), deg=1)
    label = '${%.2f} \cdot x^{%.2f}$' % (np.exp(b), a)
    print('[fit] estimate', label)
    pl.plot(xs, ys, c='r', alpha=0.5, label='data')
    pl.plot(xs, np.exp(b)*xs**a, c='b', alpha=0.5,
            label=label)
    pl.legend(loc='best')
    pl.show()


def argmin_random_tie(x):
    "argmin with randomized tie breaking."
    return np.random.choice(np.flatnonzero(x == x.min()))


def argmax_random_tie(x):
    "argmax with randomized tie breaking."
    return np.random.choice(np.flatnonzero(x == x.max()))


def onehot(i, n):
    """
    Create a one-hot vector: a vector of length `n` with a `1` at position `i`
    and zeros elsewhere.
    """
    x = np.zeros(n)
    x[i] = 1
    return x


def wls(A, b, w):
    "weighted least-squares estimation."
    from statsmodels.api import WLS
    # Note: statsmodel is a bit more accurate than directly calling lstsq
    return WLS(b, A, weights=w).fit().params


def blocks(M, k):
    """Partition the matrix M into blocks

      M = [[A, B],
           [C, D]]

    Output: `A: k x k`, `D: (n-k) x (n-k)` if `M: n x n`.

    TODO: support arbitrary partitions when `k` is a list

    """

#    if isinstance(k, list) or (isinstance(k, np.ndarray) and k.dtype == int):
#        N,M = M.shape
#        M = M[k,k]    # Shuffle the rows so that k comes first
#        nodes = set(k)
#        I = list(sorted(nodes))
#        O = list(sorted(set(range(N)) - nodes))
#        A,B,C,D = [{} for _ in range(4)]
#        for i in range(N):
#            for j in range(M):
#                v = M[i,j]
#                if i in nodes:
#                    if j in nodes:
#                        A[i,j] = v
#                    else:
#                        B[i,j] = v
#                else:
#                    if j in nodes:
#                        C[i,j] = v
#                    else:
#                        D[i,j] = v
#        k = len(k)

    assert isinstance(k, int)
    return [
        [M[:k,:k], M[:k,k:]],
        [M[k:,:k], M[k:,k:]],
    ]


class subspace:
    """
    Linear subspace
    """
    def __init__(self, A):
        # A is a collection of column vectors
        [self.dim, _] = A.shape
        self.A = A
        self.P = la.pinv(A) @ A
#        self.P = A @ la.inv(A.T @ A) @ A.T
        self.N = la.null_space(A.T)

    def project(self, q):
        return self.P @ q

    def basic_checks(self):
        # basic checks: P is a projection matrix
        P = self.P
        assert P.shape == (self.dim, self.dim)
        assert np.allclose(P, P.T)
        assert np.allclose(P @ P, P)

    def visualize(self, ax, num=100):
        if self.dim == 2:
            X = np.linspace(*ax.get_xlim(), num=num)
            a,b = self.N   # Show the linear subspace spanned by the basis vectors in F.
            ax.plot(X, -a*X/b, color='k', alpha=0.25)
        if self.dim == 3:
            X = np.linspace(*ax.get_xlim(), num=num)
            Y = np.linspace(*ax.get_ylim(), num=num)
            X,Y = np.meshgrid(X, Y)
            a,b,c = self.N   # Show the linear subspace spanned by the basis vectors in F.
            ax.plot_surface(X, Y, np.array([-(a*x+b*y)/c for x,y in zip(X.flat,Y.flat)]).reshape(X.shape),
                            color='k', alpha=0.25)
        return ax


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
    if not isfinite(x).all(): return np.nan
    return la.norm(x, p)


def zero_retrieval(want, have):
    "How good are we at retrieving zero values? Measured with F1 score."
    assert want.shape == have.shape
    return f1(want == 0, have == 0)


def f1(A, B):
    """
    Compute the F1 measure on two bit vectors.

    >>> f1([1], [1])
    1.0

    >>> f1([1], [0])
    0.0

    >>> f1([1,0,1], [0,1,1])
    0.5

    """

    A = np.array(A, dtype=bool); B = np.array(B, dtype=bool)

    C = (A & B).sum()
    A = A.sum()
    B = B.sum()
    R = C / A if A != 0 else 1.0
    P = C / B if B != 0 else 1.0
    F = 2*P*R/(P+R) if (P+R) != 0 else 1.0
    return F


def relative_difference(a, b):
    """Element-wise relative difference of two arrays

    $$
    \begin{cases}
    0                        & \mathrm{if } x = y = 0 \\
    |x-y| / \max(|x|, |y|)   & \mathrmPotherwise}`
    \end{cases}
    $$

    Choices for denominator include:

      - $\max(|x|, |y|)$: problem with $x=y=0$

      - $\mathrm{avg}(x, y)$: problem with $x = -y$; gives geometric mean

      - $\mathrm{avg}(|x|, |y|)$: problem when $x=y=0$

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


def cumavg(x):
    """
    Cumulative average.

    >>> cumavg([1,2,3,4,5])
    array([1. , 1.5, 2. , 2.5, 3. ])

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

def bernstein(samples, delta, R, check=True):
    """Plug-n-chug empirical Bernstein bound, computes "error bars" which hold with
    probability `1-δ` for the mean of independent samples from a given range
    `R=b-a` (known a priori).

    Returns ε such that the following bound hold,

      `p( mean(samples) - true_mean ≤ ε ) ≥ 1-δ`

    We assume that sample are independent (not necessarily identically
    distributed).

    Bound is based on sample variance `V` and a priori knowledge that RVs in are
    in the range `[a,b]` (although we only really require a known range `b-a`)

    The bound holds with probability `≥(1-δ)`.

    The sample mean has symmetric deviations so we get a two-sided bound by
    passing in 2*δ, i.e.,

      `p( |mean(samples) - true_mean| ≤ ε ) ≥ 1-2*δ`

    This is analogous to p-values, which make assumption of normally distributed
    random variables. This means that the bounds can be 'tighter', but the
    assumptions are usually not valid.

    """
    n = len(samples)
    if n <= 1: return np.nan
    V = np.var(samples, ddof=1)   # sample variance
    if check and np.ptp(samples) > R:
        raise ValueError(f'Sample range exceeded declared bound `{np.ptp(samples)} > {R}`')
    return sqrt(V*2*log(2.0/delta)/n) + R*(7.0/3.0)*log(2.0/delta)/(n-1)


def normalize(x, p=1):
    return x / norm(x, p)


def lidstone(p, delta):
    """
    Lidstone smoothing is a generalization of Laplace smoothing.
    """
    return normalize(p + delta)


@np.vectorize
def log1pexp(x):
    """
    Numerically stable implementation of log(1+exp(x)) aka softmax(0,x).

    -log1pexp(-x) is log(sigmoid(x))
    """
    if x <= -37:
        return exp(x)
    elif -37 <= x <= 18:
        return log1p(exp(x))
    elif 18 < x <= 33.3:
        return x + exp(-x)
    else:
        return x


@np.vectorize
def logsubexp(x, y):
    """
    Numerically stable computation of subtraction in log-space
    z = log(exp(x) - exp(y))
    """
    if x == y:
        return -np.inf
    elif x < y:
        return np.nan
    else:
        return x + log1mexp(y-x)


@np.vectorize
def log1mexp(x):
    """
    Numerically stable implementation of log(1-exp(x))

    Note: function is finite for x < 0.

    Source:
    http://cran.r-project.org/web/packages/Rmpfr/vignettes/log1mexp-note.pdf
    """
    if x >= 0:
        return np.nan
    else:
        a = abs(x)
        if 0 < a <= 0.693:
            return np.log(-np.expm1(-a))
        else:
            return np.log1p(-np.exp(-a))


# based on implementation from scikits-learn
def logsumexp(arr, axis=None):
    """Computes the sum of arr assuming arr is in the log domain.

    Returns log(sum(exp(arr))) while minimizing the possibility of
    over/underflow.

    Examples:

    >>> a = arange(10)
    >>> log(sum(exp(a)))
    9.45862974442671

    >>> logsumexp(a)
    9.45862974442671

    >>> x = [[0, 0, 1000.0], [1000.0, 0, 0]]
    >>> logsumexp(x, axis=1)
    array([1000., 1000.])

    >>> logsumexp(x)
    1000.6931471805599

    >>> logsumexp(x, axis=0)
    array([1.00000000e+03, 6.93147181e-01, 1.00000000e+03])

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


def hardmax(x):
    p = np.zeros_like(x)
    p[x.argmax()] = 1
    return p


def simpless(w, B):
    """
    Reparameterization transform similar to softmax, but for the constraints set
      ${p | p ≥ 0, sum(p) ≤ B}.$
    """

    # Assuming B = 1,
    # pi = exp(xi) / 1 + sum_j exp(xj)
    #    = exp(xi - b) * exp(b) / exp(b)*exp(-b) + sum exp(xj - b) * exp(b)
    #    = exp(xi - b) / exp(-b) + sum_j exp(xj - b)

    b = w.max()
    e = np.exp(w - b)
    return B * e / (np.exp(-b) + e.sum())


def softmax(x, axis=None):
    """
    Compute softmax avoiding numerical overflow using [this
    trick](https://timvieira.github.io/blog/post/2014/02/11/exp-normalize-trick/).

    >>> x = [1, -10, 100, .5]
    >>> softmax(x)
    array([1.01122149e-43, 1.68891188e-48, 1.00000000e+00, 6.13336839e-44])

    >>> exp(x) / exp(x).sum()
    array([1.01122149e-43, 1.68891188e-48, 1.00000000e+00, 6.13336839e-44])

    >>> x = [[0, 0, 1000], [1000, 0, 0]]

    Normalize by row:

      >>> softmax(x, axis=0)
      array([[0. , 0.5, 1. ],
             [1. , 0.5, 0. ]])

    Normalize by column:

      >>> softmax(x, axis=1)
      array([[0., 0., 1.],
             [1., 0., 0.]])

    Normalize by cell:

      >>> softmax(x, axis=None)
      array([[0. , 0. , 0.5],
             [0.5, 0. , 0. ]])

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


# TODO: add support for the axis argument.
def d_softmax(out, x, adj):
    """
    out = softmax(x), adj are the adjoints we are chaining together.

      `    A(x) = logsumexp(x)`
      `∇  A(x) = softmax(x)`
      `∇² A(x) = d_softmax(x)`   % this method.

    """
    g = adj - adj @ out
    g *= out
    return g


# TODO: move elsewhere (test cases for this method live with my proximal
# operators).  This method should probably move there.
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


def project_pmin_simplex(p, pmin):
    q = pmin * np.ones_like(p)    # assumes all actions fire.
    c = 1
    while True:
        A0 = (pmin >= c * p)
        l = p[~A0].sum()
        if l == 0: break
        Δ = q[A0].sum()
        cc = (1 - Δ) / l
        if c == cc or not np.isfinite(cc): break
        c = cc
    return np.maximum(q, c * p)


log_of_2 = log(2)


# TODO: Create discrete distribution with an entropy method an make this a
# shortcut to the method on that instance.  Similarly for `kl_divergence` and
# `mutual information`, and `cross_entropy`.
def entropy(p):
    "Entropy of a discrete random variable with distribution `p`"
    assert len(p.shape) == 1
    p = p[p.nonzero()]
    return -p @ log(p) / log_of_2


def d_entropy(p):
    return -(1/np.log(2) + np.log2(p))


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
    return -p @ log(q) / log_of_2


def assert_isdistr(p):
    assert (p >= 0).all()
    assert (p <= 1).all()
    assert abs(p.sum() - 1.0) < 0.000001


#def equal(a, b, tol=1e-10):
#    "L_{\inf}(a - b) < tol"
#    return inf_norm(a,b) < tol


def inf_norm(a, b):
    return abs(a - b).max()


# TODO: generalize to arrays? (or just use `compare`?)
def assert_equal(a, b, name='', verbose=False, throw=True, tol=0.001, color=1):
    """isfinite: asserts that *both* `a` and `b` must be finite.

    >>> assert_equal(0, 1, throw=0, color=0)
    0 1 err=[1.] fail

    >>> assert_equal(0, 0, verbose=1, color=0)
    0 0 err=[0] ok

    """
    try:
        assert not np.isnan(a).any() and not np.isnan(b).any()
    except (TypeError, AssertionError):
        pre = {"%s: " % name if name else ""}
        msg = f'{pre}want {a}, have {b}'
        if throw:
            raise AssertionError(msg)
        else:
            print(msg)

    a = np.asarray(a); b = np.asarray(b)
    err = relative_difference(a, b)
    if name:
        name = '%s: ' % name
    if verbose or np.any(err > tol):
        msg = f'{name}{a} {b} err={err}'
        if throw and err > tol:
            raise AssertionError(msg + ' ≥ tolerance (%s)' % tol)
        else:
            if not color:
                print(msg, 'ok' if err < tol else 'fail', sep=' ')
            else:
                print(msg, colors.green % 'ok' if err < tol else colors.red % 'fail', sep=' ')


def quadratic_formula(a,b,c):
    assert a != 0, 'this is a linear function!'
    return [
        (-b + np.sqrt(b**2 - 4*a*c)) / (2*a),
        (-b - np.sqrt(b**2 - 4*a*c)) / (2*a),
    ]


if __name__ == '__main__':

    def run_tests():

        from arsenal.maths import random_dist, fdcheck

        p = random_dist(30)
        fdcheck(lambda: entropy(p), p, d_entropy(p), throw=False)

        # To test the random state we'll run the function below from the same
        # random state using the restore_randome_state util.
        def foo():
            return [(random.randint(0, 100),
                     np.random.randint(0, 100))
                    for _ in range(10)]

        # Note that we have to run `a` and `b` in this order.
        with restore_random_state():
            a = foo()
        b = foo()
        assert a == b

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
            assert mutual_information(multiply.outer(px, py)) <= 1e-10

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

    import doctest
    doctest.testmod()
