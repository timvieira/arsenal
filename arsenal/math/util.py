from __future__ import division
import numpy as np
import pylab as pl
from numpy import array, exp, log, dot, abs, multiply, cumsum, arange, \
    asarray, ones, mean, searchsorted, sqrt, isfinite
from numpy.random import uniform, normal
from scipy.linalg import norm as _norm
from scipy import stats
from arsenal.terminal import yellow, green, red
from arsenal.iterview import progress
from pandas import DataFrame
from scipy.stats import pearsonr, spearmanr


def split_ix(N, p, randomize=1):
    if randomize:
        I = np.random.permutation(N)
    else:
        I = range(N)
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


class compare(object):

    def __init__(self, expect, got, name=None, data=None, P_LARGER=0.9,
                 regression=True, ax=None, alphabet=None,
                 expect_label=None, got_label=None, verbose=1):
        """Compare vectors.

        Arguments:

          - Specifying data for comparison two methods:

            1) `expect`, `got`: two numeric one-dimensional arrays which we'd like
               to compare (the argument names come for software testing). This
               method requires argument `data=None`.

            2) `data`: instance of `DataFrame`, expects arguments `expect` and `got`
               to be column labels.

          - `name`: name of this comparison.

        Note:

         - when plotting `expect` is the y-axis, `got` is the x-axis. This is by
           convention that `expect` is the dependent variable (regression target).

        TODO:

         - Allow user to specify alternative names to `expect` and `got` since they
           are often confusing.

         - Add an option to drop NaNs and continue comparison.

         - Support dictionarys as input with named dimensions and/or possibly an
           alphabet for naming dimensions.

         - Indicate which dimensions have the largest errors.

        """

        if isinstance(expect, dict) and isinstance(got, dict):
            _alphabet = expect.keys() if alphabet is None else alphabet
            assert set(got.keys()) == set(_alphabet)
            expect = [expect[k] for k in _alphabet]
            got = [got[k] for k in _alphabet]

        if data is not None:
            assert isinstance(expect, (int, basestring)), \
                'expected a column name got %s' % type(expect)
            assert isinstance(got, (int, basestring)), \
                'expected a column name got %s' % type(got)

            if expect_label is None:
                expect_label = expect
            if got_label is None:
                got_label = got

            expect = data[expect]
            got = data[got]

        else:
            if expect_label is None:
                expect_label = 'expect'
            if got_label is None:
                got_label = 'got'

            expect = asarray(expect)
            got = asarray(got)

            data = DataFrame({expect_label: expect, got_label: got})

        assert expect.shape == got.shape
        [n] = expect.shape

        self.expect = expect
        self.got = got
        self.alphabet = alphabet
        self.ax = ax
        self.name = name
        self.got_label = got_label
        self.expect_label = expect_label
        self.n = n
        self.coeff = None

        self.tests = tests = []

        # Check that vectors are finite.
        if not isfinite(expect).all():
            tests.append(['expect finite', progress(isfinite(expect).sum(), n), False])
        if not isfinite(got).all():
            tests.append(['got finite', progress(isfinite(got).sum(), n), False])

        ne = norm(expect)
        ng = norm(got)
        ok = abs(ne-ng)/ne < 0.01
        tests.append(['norms', '[%g, %g]' % (ne, ng), ok])

        # TODO: what do we want to say about sparsity?
        #tests.append(['zeros', '%s %s' % (progress((expect==0).sum(), n),
        #                                  progress((got==0).sum(), n)),
        #              -1])
        F = zero_retrieval(expect, got)
        tests.append(['zero F1', F, F > 0.99])

        c = cosine(expect, got)
        self.cosine = c
        tests.append(['cosine-sim', c, (c > 0.99999)])   # cosine similarities must be really high.

        self.pearsonr = 1.0 if ne == ng == 0 else pearsonr(expect, got)[0]
        tests.append(['pearson', self.pearsonr, (self.pearsonr > 0.99999)])

        p = spearmanr(expect, got)[0]
        tests.append(['spearman', p, (p > 0.99999)])

        # TODO: this check should probably take into account the scale of the data.
        d = linf(expect, got)
        self.max_err = d
        tests.append(['Linf', d, d < 1e-8])

        # same sign check (weak agreement, but useful sanity check -- especially
        # for gradients)
        x = expect
        y = got
        s = asarray(~((x >= 0) ^ (y >= 0)), dtype=int)
        p = s.sum() * 100.0 / len(s)
        tests.append(['same-sign', '%s%% (%s/%s)' % (p, s.sum(), len(s)), p == 100.0])

        # relative error
        r = relative_difference(expect, got)
        r = mean(r[isfinite(r)])
        tests.append(['mean relative error', r, r <= 0.01])

        # TODO: suggest that if relative error is high and rescaled error is low (or
        # something to do wtih regression residuals) that maybe there is a
        # (hopefully) simple fix via scale/offset.

        # TODO: can provide descriptive statistics for each vector
        #tests.append(['range (expect)', [expect.min(), expect.max()], 2])
        #tests.append(['range (got)   ', [got.min(), got.max()], 2])

        # regression and rescaled error only valid for n >= 2
        if n >= 2:
            es = abs(expect).max()
            gs = abs(got).max()
            if es == 0:
                es = 1
            if gs == 0:
                gs = 1
            # rescaled error
            E = expect / es
            G = got / gs
            R = abs(E - G)
            r = mean(R)
            tests.append(['mean rescaled error', r, r <= 1e-5])

        if regression:
            self.regression()

        if n >= 2:
            # These tests check if one of the datasets is consistently larger than the
            # other. The threshold for error is based on `P_LARGER` ("percent larger").
            L = ((expect-got) > 0).sum()
            if L >= P_LARGER * n:
                tests.append(['expect is larger', progress(L, n), 0])
            L = ((got-expect) > 0).sum()
            if L >= P_LARGER * n:
                tests.append(['got is larger', progress(L, n), 0])

        self.tests = tests
        if verbose:
            self.message()

        if alphabet is not None:
            self.show_largest_rel_errors()

    def message(self):
        print
        print 'Comparison%s:' % (' (%s)' % self.name if self.name else ''), 'n=%s' % self.n
        #print yellow % 'expected:'
        #print expect
        #print yellow % 'got:'
        #print got
        for k, v, passed in self.tests:
            if passed == 1:
                c = green
            elif passed == 0:
                c = red
            else:
                c = yellow
            try:
                v = '%g' % v
            except TypeError:
                pass
            print '  %s: %s' % (k, c % (v,))
        print

    def plot(self, regression=True, seaborn=False, ax=None, **scatter_kw):
        if ax is not None:
            self.ax = ax
        if seaborn:
            import seaborn as sns
            sns.set_context(rc={"figure.figsize": (7, 5)})
            g = sns.JointGrid(self.got_label, self.expect_label, data=self.data)
            g.plot(sns.regplot, sns.distplot, stats.spearmanr)
            print "Pearson's r: {0}".format(self.pearsonr)
        else:
            if self.ax is None:
                self.ax = pl.figure().add_subplot(111)
            self.ax.scatter(self.got, self.expect, lw=0, alpha=0.5, **scatter_kw)
            if self.name is not None:
                self.ax.set_title(self.name)
            self.ax.set_xlabel(self.got_label)
            self.ax.set_ylabel(self.expect_label)
        if regression:
            self.regression_line()
        return self

    def show(self, *args, **kw):
        self.plot(*args, **kw)
        pl.show()
        return self

    def regression_line(self):
        # TODO: write the coeff to plot.
        if self.coeff is not None and isfinite(self.coeff).all():
            xa, xb = self.ax.get_xlim()
            A = ones((self.n, 2))
            A[:,0] = self.got
            # plot estimated line
            ys = A.dot(self.coeff)
            self.ax.plot(A[:,0], ys, c='r', alpha=0.5)
            self.ax.grid(True)
            self.ax.set_xlim(xa,xb)
        return self

    def regression(self):
        "least squares linear regression"

        # TODO: for regression we want parameters `[1 0]` and a small
        # residual. We want both these conditions to hold. Might be
        # useful to look at R^2 statistic since it normalizes scale and
        # number of data-points. (it's often used for reduction in
        # variance.)

        # data can't contain any NaNs
        if not isfinite(self.got).all() or not isfinite(self.expect).all():
            self.tests.append(['regression',
                               'did not run due to NaNs in data',
                               0])
            return

        if self.n < 2:
            self.tests.append(['regression',
                               'too few points',
                               0])
            return

        from scipy.linalg import lstsq
        A = ones((self.n, 2))
        A[:,0] = self.got

        self.coeff, _, _, _ = lstsq(A, self.expect)

        # Label with warn or ok.
        ok = 1 if abs(self.coeff - [1, 0]).max() <= 1e-5 else 2

        self.tests.append(['regression', '[%.3f %.3f]' % (self.coeff[0], self.coeff[1]), ok])

    def show_largest_rel_errors(self):
        "show largest relative errors"

        df = []

        #es = abs(expect).max()
        #gs = abs(got).max()

        for (i,(x,y)) in enumerate(zip(self.expect, self.got)):
            # XXX: skip zeros.
            #if abs(x) < 1e-10 and abs(y) < 1e-10:
            #    e = 0.0

            e = relative_difference(x, y)

            if e <= 0.001:
                continue

            df.append([e, self.alphabet[i], x, y])

            #df.append({'name':   alphabet[i],
            #           'error':  e,
            #           'expect': x,
            #           'got':    y})

        df.sort(reverse=1)

        if len(df):
            print ' Relative errors'
            print ' ==============='
            for e, n, x, y in df:

                types = []
                if x < y:
                    types.append('bigger')
                else:
                    types.append('smaller')

                # highlight sign errors.
                #if np.sign(x) != np.sign(y):
                if (x >= 0) != (y >= 0):
                    types.append(red % 'wrong sign')

                print '  %-15s %.5f %g %g' % (n, e, x, y), \
                    ((green % 'ok') if e <= 0.01 else red % 'bad'), \
                    '(%s)' % (', '.join(types))

        #from pandas import DataFrame
        #df = DataFrame(df)
        #df.set_index('name', inplace=1)
        #print df.sort('error', ascending=0)


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
    return sample(exp(w - w.max()))


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

    >>> a = arange(10)
    >>> log(sum(exp(a)))
    9.4586297444267107
    >>> logsumexp(a)
    9.4586297444267107
    """
    arr = np.array(arr, dtype=np.double)
    arr = np.rollaxis(arr, axis)
    # Use the max to normalize, as with the log this is what accumulates the
    # less errors
    vmax = arr.max(axis=0)
    arr -= vmax
    exp(arr, out=arr)
    out = log(arr.sum(axis=0))
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
    exp(y, y)
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


def assert_equal(a, b, name='', verbose=False, throw=True, tol=1e-10, color=1):
    """isfinite: asserts that *both* `a` and `b` must be finite.

    >>> assert_equal(0, 1, throw=0, color=0)
    0 1 err=1 fail

    >>> assert_equal(0, 0, verbose=1, color=0)
    0 0 err=0 ok

    """
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
                print msg, 'ok' if err < tol else 'fail'
            else:
                print msg, green % 'ok' if err < tol else red % 'fail'


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


        print 'passed tests.'

    run_tests()

    def test_compare():
        n = 100
        # `a` is a noisy version of `b`, but tends to overestimate.
        a = np.linspace(0,1,n)
        b = a + np.random.uniform(-0.01, 0.1, size=n)
        compare(a,b,scatter=1)
        compare('a', 'b', scatter=1, data=DataFrame({'a': a, 'b': b}))
        pl.show()

    #test_compare()

    print relative_difference(np.inf, np.inf)
