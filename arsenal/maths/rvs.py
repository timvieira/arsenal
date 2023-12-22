import numpy as np
import matplotlib.pyplot as pl
import scipy.stats as st
from numpy import array, exp, cumsum, asarray
from numpy.linalg import norm
from scipy.integrate import quad


def is_distribution(p):
    p = asarray(p)
    return (p >= 0).all() and abs(1 - p.sum()) < 1e-10


def anneal(p, *, invT=None, T=None):
    "p ** (1/T)"
    if T is not None:
        assert invT is None
        invT = 1./T
    p = p ** invT
    p /= p.sum()
    return p


class Max:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def cdf(self, t):
        return self.X.cdf(t)*self.Y.cdf(t)

    def pdf(self, t):
        X = self.X; Y = self.Y
        #  d/dt[cdf(t)] = d/dt[X.cdf(t)*Y.cdf(t)]
        #               = X.cdf(t)*d/dt[Y.cdf(t)] + d/dt[X.cdf(t)]*Y.cdf(t)
        #               = X.cdf(t)*Y.pdf(t) + X.pdf(t)*Y.cdf(t)
        return X.pdf(t)*Y.cdf(t) + X.cdf(t)*Y.pdf(t)

    def ppf(self, u):
        raise ValueError('no closed form for ppf(max(X,Y))')

    def rvs(self, size):
        return np.maximum(self.X.rvs(size), self.Y.rvs(size))


class _BruteForce:
    """
    Base class for tabular representation of a distribution

      p(x) ∝ score(x).

    where score(x) > 0 for all x ∈ domain.

    """

    def __init__(self):
        self.Z = np.sum([self.score(x) for x in self.domain()])
        self.P = {x: self.score(x) / self.Z for x in self.domain()}

    def domain(self):
        raise NotImplementedError

    def score(self, x):
        raise NotImplementedError()

    def entropy(self):
        return -np.sum([p * np.log(p) for p in self.P.values() if p != 0])

    def logp(self, x):
        return np.log(self.P[x])


class TruncatedDistribution:
    def __init__(self, d, a, b):
        assert np.all(a <= b), [a, b]
        self.d = d; self.a = a; self.b = b
        self.cdf_b = d.cdf(b)
        self.cdf_a = d.cdf(a)
        self.cdf_w = self.cdf_b - self.cdf_a
    def sf(self, x):
        return 1-self.cdf(x)
    def pdf(self, x):
        return (self.a < x) * (x <= self.b) * self.d.pdf(x) / self.cdf_w
    def rvs(self, size=None):
        u = np.random.uniform(0, 1, size=size)
        return self.ppf(u)
    def ppf(self, u):
        return self.d.ppf(self.cdf_a + u * self.cdf_w)
    def cdf(self, x):
        return np.minimum(1, (self.a < x) * (self.d.cdf(x) - self.cdf_a) / self.cdf_w)
    def mean(self):
        # The truncated mean is unfortunately not analytical
        return quad(lambda x: x * self.pdf(x), self.a, self.b)[0]

        # XXX: The Darth Vader only applies to positive random variables
        # http://thirdorderscientist.org/homoclinic-orbit/2013/6/25/the-darth-vader-rule-mdash-or-computing-expectations-using-survival-functions
        # https://content.sciendo.com/view/journals/tmmp/52/1/article-p53.xml
#        return quad(self.sf, self.a, self.b)[0] + self.a



# References
#
#  - Hypoexponential
#    https://en.wikipedia.org/wiki/Hypoexponential_distribution
#
#  - Márton Balázs, https://people.maths.bris.ac.uk/~mb13434/sumexp.pdf
#
#  - Bibinger (2013) "Notes on the sum and maximum of independent exponentially
#    distributed random variables with different scale parameters"
#
#  - https://actuarialmodelingtopics.wordpress.com/2016/08/01/the-hyperexponential-and-hypoexponential-distributions/
#
class SumOfExponentials:
    def __init__(self, w):
        self.w = w
        [self.n] = w.shape
        self.a = np.prod(w)
        self.B = np.array([np.prod([w[j] - w[i] for j in range(self.n) if j != i]) for i in range(self.n)])
    def cdf(self, x):
        return 1-self.a*sum(np.exp(-self.w[j]*x) / (self.w[j] * self.B[j]) for j in range(self.n))
    def pdf(self, x):
        return self.a * sum(np.exp(-self.w[j]*x) / self.B[j] for j in range(self.n))
    def rvs(self, size=None):
        if size is not None: size = (size, self.n)
        return -np.sum(np.log(np.random.uniform(0,1,size=size)) / self.w[None,:], axis=1)
    def mgf(self, t):
        return self.a / np.product(self.w - t)
    def d_mgf(self, t, n):
        # TODO: work out the derivative
        return nd.Derivative(self.mgf, n=n)(t)
    def mean(self):
        return np.sum(1/self.w) # sum of the means
    def var(self):
        return np.sum(1/self.w**2) # sum of the variances because they are indep


def show_distr(D, a, b, resolution=1000):
    xs = np.linspace(a, b, resolution)
    us = np.linspace(0, 1, resolution)
    fig, ax = pl.subplots(figsize=(12,4), ncols=3)

    if hasattr(D, 'pdf'):
        ax[0].plot(xs, D.pdf(xs))
        ax[0].set_ylabel('f(x)')
        ax[0].set_xlabel('x')
        ax[0].set_title('probability density function')
        ax[0].set_xlim(a, b)

    ax[1].plot(xs, D.cdf(xs))
    ax[1].set_ylabel('F(x)')
    ax[1].set_xlabel('x')
    ax[1].set_title('cumulative distribution function')
    ax[1].set_xlim(a, b)


    if hasattr(D, 'ppf'):
        ax[2].plot(us, D.ppf(us))
        ax[2].set_ylabel('$F^{-1}(u)$')
        ax[2].set_xlabel('u')
        ax[2].set_xlim(0, 1)
        ax[2].set_title('quantile function')

    fig.tight_layout()

    for a in ax:
        # Move left and bottom spines outward by 10 points
        a.spines['left'].set_position(('outward', 10))
        a.spines['bottom'].set_position(('outward', 10))
        # Hide the right and top spines
        a.spines['right'].set_visible(False)
        a.spines['top'].set_visible(False)
        # Only show ticks on the left and bottom spines
        a.yaxis.set_ticks_position('left')
        a.xaxis.set_ticks_position('bottom')

    return ax


def compare_samples_to_distr(D, samples, a, b, bins):

    fig, ax = pl.subplots(figsize=(12,4), ncols=3)

    ax[0].hist(samples, bins=bins, color='b', alpha=0.5, density=True,
               label='histogram')

    xs = np.linspace(a, b, 1000)
    ax[0].plot(xs, D.pdf(xs), c='k')
    ax[0].set_title('pdf')

    E = Empirical(samples)

    ax[1].plot(xs, E.cdf(xs), alpha=0.5, linestyle=':')
    ax[1].plot(xs, D.cdf(xs), alpha=0.5)
    ax[1].set_title('cdf')

    us = np.linspace(0, 1, 1000)
    ax[2].plot(us, E.ppf(us), alpha=0.5, linestyle=':')
    ax[2].plot(us, [D.ppf(u) for u in us], alpha=0.5)
    ax[2].set_title('ppf')

    for a in ax:
        # Move left and bottom spines outward by 10 points
        a.spines['left'].set_position(('outward', 10))
        a.spines['bottom'].set_position(('outward', 10))
        # Hide the right and top spines
        a.spines['right'].set_visible(False)
        a.spines['top'].set_visible(False)
        # Only show ticks on the left and bottom spines
        a.yaxis.set_ticks_position('left')
        a.xaxis.set_ticks_position('bottom')

    fig.tight_layout()

    return ax


def test_truncated_distribution():
    import matplotlib.pyplot as pl
    import scipy.stats as st
    d = st.lognorm(1.25)

    t = TruncatedDistribution(d, 2, 4)

    print(t.mean(), t.rvs(100_000).mean())

    if 1:
        us = np.linspace(0.01, 0.99, 1000)
        xs = np.linspace(d.ppf(0.01), d.ppf(0.99), 1000)
        pl.plot(xs, t.cdf(xs), label='cdf')
        pl.plot(t.ppf(us), us, label='ppf')
        pl.legend(loc='best')
        pl.xlim(0, 6)
        pl.show()

    if 1:
        pl.hist(t.rvs(100000), density=True, bins=200)
        pl.plot(xs, t.pdf(xs), c='r', lw=3, alpha=0.75)
        pl.xlim(0, 6)
        pl.show()

    if 1:
        us = np.linspace(0.01, 0.99, 100)
        for u in us:
            v = t.cdf(t.ppf(u))
            assert abs(u - v)/abs(u) < 1e-3

    if 1:
        xs = np.linspace(1, 5, 1000)
        for x in xs:
            y = t.ppf(t.cdf(x))
            if t.pdf(x) > 0:
                err = abs(x - y)/abs(x)
                assert err < 1e-3, [err, x, y]


def random_dist(*size):
    """
    Generate a random conditional distribution which sums to one over the last
    dimension of the input dimensions.
    """
    return np.random.dirichlet(np.ones(size[-1]), size=size[:-1])


def random_psd(n):
    return st.wishart.rvs(df=n, scale=np.eye(n)) / n


class Mixture(object):
    """
    Mixture of several densities
    """
    def __init__(self, w, ds):
        w = array(w)
        assert is_distribution(w), \
            'w is not a prob. distribution.'
        self.ds = ds
        self.w = w

    def rvs(self, size=1):
        # sample component
        i = sample(self.w, size=size)
        # sample from component
        return array([self.ds[j].rvs() for j in i])

    def pdf(self, x):
        return sum([d.pdf(x) * w for w, d in zip(self.w, self.ds)])

    def ppf(self, q):
        from scipy.optimize import minimize
        x0 = sum([d.ppf(q) * w for w, d in zip(self.w, self.ds)])
        return minimize(lambda t: np.sum((self.cdf(t) - q)**2), x0).x

    def cdf(self, x):
        return sum([d.cdf(x) * w for w, d in zip(self.w, self.ds)])

    def mean(self):
        return sum([d.mean() * w for w, d in zip(self.w, self.ds)])


def spherical(size):
    "Generate random vector from spherical Gaussian."
    x = np.random.normal(0, 1, size=size)
    x /= norm(x, 2)
    return x



# TODO: Should we create a class to represent this data with this the fit
# method?  This should really be the MLE of some sort of distrbution.  What
# distribution is it?  I suppose it is nonparametric in the same sense that
# Kaplan-Meier is nonparametric (In fact, KM generalizes this estimator to
# support censored response).
# TODO: That same class would probably have the defacto mean/std estimators.
class Empirical:
    """
    Empirical CDF of data `a`, returns function which makes values to their
    cumulative probabilities.

     >>> g = cdf([5, 10, 15])

    Evaluate the CDF at a few points

     >>> g([5,9,13,15,100])
     array([0.33333333, 0.33333333, 0.66666667, 1.        , 1.        ])


    Check that ties are handled correctly

     >>> g = cdf([5, 5, 15])

     The value p(x <= 5) = 2/3

     >>> g([0, 5, 15])
     array([0.        , 0.66666667, 1.        ])

    The auantile function should be the inverse of the cdf.

      >>> g = cdf([-1, 5, 5, 15])
      >>> g.quantile(np.linspace(0, 1, 10))
      array([-1, -1, -1,  5,  5,  5,  5,  5,  5, 15])

    """

    def __init__(self, x):
        self.x = x = np.array(x, copy=True)
        [self.n] = x.shape
        self.x.sort()

    def __call__(self, z):
        return self.x.searchsorted(z, 'right') / self.n

    cdf = __call__

    def sf(self, z):
        return 1-self.cdf(z)

    def conditional_mean(self, a, b):
        "E[T | a <= T < b]"
        m = 0.0; n = 0.0
        for i in range(self.x.searchsorted(a, 'right'),
                       self.x.searchsorted(b, 'left')):
            m += self.x[i]
            n += 1
        return m / n if n > 0 else np.inf

    def quantile(self, q):
        # TODO: this could be made fastet given that x is already sorted.
        assert np.all((0 <= q) & (q <= 1))
        return np.quantile(self.x, q, interpolation='lower')

    def plot(self, confidence=0.95):
        pl.plot(self.x, self.cdf(self.x))

        if confidence is not None:
            # show confidence bands (derived from the DKW inequality)
            # https://bjlkeng.github.io/posts/the-empirical-distribution-function/
            # https://en.wikipedia.org/wiki/Dvoretzky%E2%80%93Kiefer%E2%80%93Wolfowitz_inequality
            eps = np.sqrt(np.log(2 / (1-confidence)) / (2 * self.n))
            pl.fill_between(self.x,
                            np.maximum(0, self(self.x) - eps),   # lower
                            np.minimum(1, self(self.x) + eps),   # upper
                            alpha=0.1,
                            label=f'{confidence:.2f} confidence band')

    ppf = quantile

cdf = Empirical


def sample(w, size=None, u=None):
    """
    Uses the inverse CDF method to return samples drawn from an (unnormalized)
    discrete distribution.
    """
    c = cumsum(w)
    if u is None:
        u = np.random.uniform(0,1,size=size)
    return c.searchsorted(u * c[-1])


def log_sample(w):
    "Sample from unnormalized log-distribution."
    a = np.array(w, dtype=float)
    a -= a.max()
    exp(a, out=a)
    return sample(a)


def sample_dict(x, *args, **kwargs):
    "Sample keys from `x` in proportion to their values."
    keys = np.array(list(x.keys()))
    vals = np.array(list(x.values()))
    return keys[sample(vals, *args, **kwargs)]


def test_mixture():

    d = [st.norm(1, 2), st.norm(2, .5), st.norm(3, .1)]

    w = np.array([.2, .7, .1])

    D = Mixture(w, d)

    S = D.rvs(100_000)

    assert abs(D.mean() - S.mean()) < 0.005, abs(D.mean() - S.mean())

    a, b = -5, 5

    compare_samples_to_distr(D, S, a, b, bins=100)
    pl.show()

#    if 1:
#        us = np.linspace(0.01, 0.99, 100)
#        for u in us:
#            v = D.cdf(D.ppf(u))
#            err = abs(u - v)/abs(u)
#            assert err < 1e-3, err
#
#    if 1:
#        xs = np.linspace(a, b, 100)
#        for x in xs:
#            y = D.ppf(D.cdf(x))
#            if D.pdf(x) > 0:
#                err = abs(x - y)/abs(x)
#                assert err < 1e-3, [err, x, y]


def test_cdf():
    n = 1_000
    x = np.random.normal(0,1,size=n)
    cdf(x).plot()
    pl.legend(loc='best')
    pl.show()


def test_sample_dict():

    ws = {'a': 9, 'b': 1, 'c': 0}
    W = sum(ws.values())

    xs = sample_dict(ws, size=10)
    assert len(xs) == 10

    N = 1_000_000
    xs = sample_dict(ws, size=N)
    from collections import Counter
    c = Counter(xs)
    for x in ws:
        print(ws[x]/W, c[x]/N)
        assert abs(ws[x]/W - c[x]/N) <= 0.001

    x = sample_dict(ws, u=.5)
    assert x == 'a'

    x = sample_dict(ws, u=.91)
    assert x == 'b'


if __name__ == '__main__':
    #test_truncated_distribution()
    #test_mixture()
    from arsenal import testing_framework
    testing_framework(globals())
