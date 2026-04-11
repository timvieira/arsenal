import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from arsenal.maths.pareto import pareto_frontier, show_frontier


def test_pareto_frontier_max_max():
    """maxX=True, maxY=True: upper-right frontier."""
    X = [1, 2, 3, 2]
    Y = [3, 2, 1, 1]
    f = pareto_frontier(X, Y, maxX=True, maxY=True)
    # (1,3) dominates nothing on both axes; (3,1) has max x; (1,3) has max y
    # Frontier should include (1,3), (2,2), (3,1) - all non-dominated
    assert (1, 3) in f
    assert (3, 1) in f


def test_pareto_frontier_min_min():
    """maxX=False, maxY=False: lower-left frontier."""
    X = [1, 2, 3, 2]
    Y = [3, 2, 1, 1]
    f = pareto_frontier(X, Y, maxX=False, maxY=False)
    assert (1, 3) in f or (2, 1) in f  # lower-left points


def test_pareto_frontier_empty():
    """Empty input returns empty frontier."""
    assert pareto_frontier([], []) == []


def test_pareto_frontier_single():
    """Single point is always on the frontier."""
    f = pareto_frontier([5], [5], maxX=True, maxY=True)
    assert f == [(5, 5)]


def test_pareto_frontier_indices():
    """indices=True returns index list."""
    X = [1, 3, 2]
    Y = [3, 1, 2]
    f = pareto_frontier(X, Y, maxX=True, maxY=True, indices=True)
    assert all(isinstance(i, int) for i in f)
    assert 0 in f  # (1,3) is on frontier
    assert 1 in f  # (3,1) is on frontier


def test_show_frontier_smoke():
    """show_frontier runs without error for all 4 max combos."""
    np.random.seed(42)
    X, Y = np.random.normal(0, 1, size=(2, 30))

    for maxX in [False, True]:
        for maxY in [False, True]:
            pl.figure()
            pts = show_frontier(X, Y, maxX=maxX, maxY=maxY)
            assert pts is not None
            assert len(pts) > 0
            pl.close()

    pl.close('all')
