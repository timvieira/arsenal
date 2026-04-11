import numpy as np
from collections import Counter

from arsenal.maths.rvs import (
    TruncatedDistribution, Mixture, cdf, sample_dict,
)


def test_truncated_distribution():
    import scipy.stats as st
    d = st.lognorm(1.25)

    t = TruncatedDistribution(d, 2, 4)

    assert abs(t.mean() - t.rvs(100_000).mean()) < 0.05

    us = np.linspace(0.01, 0.99, 100)
    for u in us:
        v = t.cdf(t.ppf(u))
        assert abs(u - v)/abs(u) < 1e-3

    xs = np.linspace(1, 5, 1000)
    for x in xs:
        y = t.ppf(t.cdf(x))
        if t.pdf(x) > 0:
            err = abs(x - y)/abs(x)
            assert err < 1e-3, [err, x, y]


def test_mixture():
    import scipy.stats as st

    d = [st.norm(1, 2), st.norm(2, .5), st.norm(3, .1)]
    w = np.array([.2, .7, .1])

    D = Mixture(w, d)
    S = D.rvs(100_000)

    assert abs(D.mean() - S.mean()) < 0.02, abs(D.mean() - S.mean())


def test_cdf():
    n = 1_000
    x = np.random.normal(0, 1, size=n)
    c = cdf(x)
    # basic sanity: CDF at min is ~0, at max is 1
    assert c(x.min()) > 0
    assert c(x.max()) == 1.0


def test_sample_dict():

    ws = {'a': 9, 'b': 1, 'c': 0}
    W = sum(ws.values())

    xs = sample_dict(ws, size=10)
    assert len(xs) == 10

    N = 1_000_000
    xs = sample_dict(ws, size=N)
    c = Counter(xs)
    for x in ws:
        assert abs(ws[x]/W - c[x]/N) <= 0.001

    x = sample_dict(ws, u=.5)
    assert x == 'a'

    x = sample_dict(ws, u=.91)
    assert x == 'b'
