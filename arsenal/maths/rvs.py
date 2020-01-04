import numpy as np
from numpy.random import uniform, normal
from numpy import array, exp, cumsum, asarray
from numpy.linalg import norm
from scipy.integrate import quad

def is_distribution(p):
    p = asarray(p)
    return (p >= 0).all() and abs(1 - p.sum()) < 1e-10


class TruncatedDistribution:
    def __init__(self, d, a, b):
        assert np.all(a <= b), [a, b]
        self.d = d; self.a = a; self.b = b
    def sf(self, x):
        return 1-self.cdf(x)
    def pdf(self, x):
        d = self.d; a = self.a; b = self.b
        return (a <= x) * (x <= b) * d.pdf(x) / (d.cdf(b) - d.cdf(a))
    def rvs(self, size=None):
        u = uniform(0, 1, size=size)
        return self.ppf(u)
    def ppf(self, u):
        d = self.d
        cdf_a = d.cdf(self.a)
        return d.ppf(cdf_a + u * (d.cdf(self.b) - cdf_a))
    def cdf(self, x):
        d = self.d; a = self.a; b = self.b
        cdf_a = d.cdf(a)
        w = d.cdf(b) - cdf_a
        return np.minimum(1, (d.cdf(x) - cdf_a) * (a <= x) / w)
    def mean(self):
        # The truncated mean is unfortunately not analytical
        return quad(lambda x: x * self.pdf(x), self.a, self.b)[0]

        # XXX: The Darth Vader only applies to positive random variables
        # http://thirdorderscientist.org/homoclinic-orbit/2013/6/25/the-darth-vader-rule-mdash-or-computing-expectations-using-survival-functions
        # https://content.sciendo.com/view/journals/tmmp/52/1/article-p53.xml
#        return quad(self.sf, self.a, self.b)[0] + self.a


def test_truncated_distribution():

    import pylab as pl
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

    def rvs(self, size=1):
        # sample component
        i = sample(self.w, size=size)
        # sample from component
        return array([self.pdfs[j].rvs() for j in i])

    def pdf(self, x):
        return sum([p.pdf(x) * w for w, p in zip(self.w, self.pdfs)])


def spherical(size):
    "Generate random vector from spherical Gaussian."
    x = normal(0, 1, size=size)
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

    ppf = quantile

cdf = Empirical


def sample(w, size=None):
    """
    Uses the inverse CDF method to return samples drawn from an (unnormalized)
    discrete distribution.
    """
    c = cumsum(w)
    r = uniform(size=size)
    return c.searchsorted(r * c[-1])


def log_sample(w):
    "Sample from unnormalized log-distribution."
    a = w - w.max()
    exp(a, out=a)
    return sample(a)


if __name__ == '__main__':
    test_truncated_distribution()
