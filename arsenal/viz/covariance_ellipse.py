###############################################################################
# drawtools.py
# Some drawing tools.
###############################################################################

import numpy as np
import pylab as pl

from scipy.constants import pi
from scipy.linalg import eig

from numpy import sqrt, arctan2


from matplotlib.patches import Ellipse


def covariance_ellipse(ax, center, covariance, nstd=4):
    """
    Draw an ellipse for a Gaussian with covariance matrix..

    Args:
        A: 2x2 matrix describing the ellipse.
        c: Centre of the ellipse.
    """

    lab, l = eig(covariance)   # use eigh because it's symmetric?

    e = Ellipse(xy = center,
                width = sqrt(lab[0])*nstd,
                height = sqrt(lab[1])*nstd,
                angle = -arctan2(l[0,1], l[0,0]) / pi * 180)

    e.set_facecolor([1, 1, 1])
    ax.add_artist(e)


def test():

    C = np.random.randn(2, 2)
    C = C.dot(C.T) + 0.1*np.eye(2)
    d = np.random.multivariate_normal(np.zeros(2), C, 1000)

    ax = pl.figure(1).add_subplot(111)
    ax.plot(d[:, 0], d[:, 1], 'x')
    covariance_ellipse(ax, center=[0,0], covariance=C)

    pl.show()


if __name__ == '__main__':
    test()
