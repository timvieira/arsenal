"""
Pareto frontier
"""
import pylab as pl
import numpy as np
from arsenal.terminal import yellow
from arsenal.iterextras import window


def pareto_frontier(X, Y, maxX=True, maxY=True):
    """Determine Pareto frontier, returns list of sorted points.

    Args:

      X, Y: data.

      maxX, maxY: (bool) whether to maximize or minimize along respective
        coordinate.

    """
    assert len(X) == len(Y)
    if len(X) == 0:
        return []
    a = sorted(zip(X, Y), reverse=maxX)
    frontier = []
    _, lasty = a[0]
    for xy in a:
        _,y = xy
        if maxY:
            if y >= lasty:
                frontier.append(xy)
                lasty = y
        else:
            if y <= lasty:
                frontier.append(xy)
                lasty = y
    return frontier


def show_frontier(X, Y, maxX=False, maxY=True, dots=False,
                  XMAX=None, YMIN=None, ax=None, label=None, **style):
    """Plot Pareto frontier.

    Args:

      X, Y: data.

      maxX, maxY: (bool) whether to maximize or minimize along respective
        coordinate.

      dots: (bool) highlight points on the frontier (will use same color as
        `style`).

      ax: use an existing axis if non-null.

      style: keyword arguments, which will be passed to lines connecting the
        points on the Pareto frontier.

      XMAX: max value along x-axis
      YMIN: min value along y-axis

    """
    if ax is None:
        ax = pl.gca()
    sty = {'c': 'b', 'alpha': 0.3, 'zorder': 0}
    sty.update(style)

    assert not maxX and maxY, 'need to update some hardcoded logic'

    f = pareto_frontier(X, Y, maxX=maxX, maxY=maxY)
    if not f:
        print yellow % '[warn] Empty frontier'
        return
    if dots:
        xs, ys = zip(*f)
        ax.scatter(xs, ys, lw=0, alpha=0.5, c=sty['c'])
    # Connect corners of frontier. The first and last points on frontier have
    # lines which surround the point cloud.
    p, q = f[0], f[-1]

    (a,b) = min(X), max(X)
    (c,d) = min(Y), max(Y)

    # connect points with line segments
    pts = []

    XMAX = XMAX if XMAX is not None else max(X)
    YMIN = YMIN if YMIN is not None else min(Y)
    assert XMAX >= max(X)
    assert YMIN <= min(Y)

    pts.extend([(min(X), YMIN)])
    pts.extend(x for ((a,b), (c,d)) in window(f, 2) for x in [[a,b], [c,b], [c,b], [c,d]])
    pts.extend([(XMAX, max(Y))])

    # make plot
    pts = np.array(pts)
    ax.plot(pts[:,0], pts[:,1], label=label, **sty)


def test():
    X = np.random.uniform(0,1,size=100)
    Y = np.random.uniform(0,1,size=100)
    pl.scatter(X, Y, c='r', lw=0)
    show_frontier(X, Y)
    pl.show()


if __name__ == '__main__':
    test()
