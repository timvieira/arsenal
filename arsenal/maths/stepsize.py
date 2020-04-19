"""
Adaptive stepsize algorithms
"""
import numpy as np


__author__ = 'Tim Vieira (http://timvieira.github.io)'


def norm_clip(x, C):
    "Rescale x (in place) so that ||x|| <= C."
    z = np.linalg.norm(x)
    if z > C:
        x[:] *= C/z


def ewma(x, y, alpha):
    "Exponentially weighted moving average (`x` is updated in place)."
    x[:] *= (1-alpha)
    x[:] += alpha*y


class adagrad(object):
    """
    Adagrad
    """
    def __init__(self, x, damping = 1e-4):
        self.x = x
        self.G = np.zeros_like(x) + damping
        self.i = 0
        self.D = None

    def __call__(self, g, learning_rate=1.0):
        # Update parameters
        self.G += g*g
        self.D = learning_rate/np.sqrt(self.G)
        self.x[:] -= g * self.D
        self.i += 1


class sgd(object):
    """
    Simple sgd
    """
    def __init__(self, x):
        self.x = x
        self.i = 0

    def __call__(self, g, learning_rate=1.0):
        self.x[:] -= g * learning_rate
        self.i += 1


class adam(object):
    """
    Adam as described in http://arxiv.org/pdf/1412.6980.pdf.
    """
    def __init__(self, x):
        self.x = x
        self.m = np.zeros_like(x)
        self.v = np.zeros_like(x)
        self.i = 1
        self.D = None

    def __call__(self, g, learning_rate=0.01, b1 = 0.1, b2 = 0.01, lam=1e-4, damping=1e-4):
        i = self.i
        b1t = 1 - (1-b1)*(lam**i)          # b1t -> 1 over time
        # Update first moment estimate
        ewma(self.m, g, b1t)
        # Update second moment estimate
        ewma(self.v, g*g, b2)
        # Bias correction.
        mhat = self.m / (1 - (1-b1)**i)
        vhat = self.v / (1 - (1-b2)**i)
        # Take step
        self.x[:] -= learning_rate*mhat/(np.sqrt(vhat) + damping)
        self.i += 1


class sgd_momentum(object):

    def __init__(self, x):
        self.velocity = np.zeros(len(x))
        self.x = x

    def __call__(self, g, mass=0.9, learning_rate=0.1):
        self.velocity[:] = mass * self.velocity - (1.0 - mass) * g
        self.x[:] += learning_rate * self.velocity
