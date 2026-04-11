import numpy as np
import matplotlib
matplotlib.use('Agg')

from arsenal.maths.bootstrapped import bootstrapped_model


def test_basics():
    np.random.seed(42)
    n = 100  # small n for speed
    xs = np.random.uniform(-5, 5, size=n)
    ys = xs * np.cos(xs * 5) + np.random.normal(0, 0.5, size=n)

    # Smoke test: should run without error and produce a plot
    bootstrapped_model(xs, ys, degree=5, n_bootstraps=50)

    # Verify matplotlib state has data
    import matplotlib.pyplot as pl
    ax = pl.gca()
    assert len(ax.lines) > 0, 'should have plotted lines'
    assert len(ax.collections) > 0, 'should have plotted scatter/fill'
    pl.close('all')
