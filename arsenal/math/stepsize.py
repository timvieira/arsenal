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
    "Exponentially weighted moving average."
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


class adam(object):
    """
    Adam as described in http://arxiv.org/pdf/1412.6980.pdf.
    """
    def __init__(self, x, damping=1e-4):
        self.x = x
        self.m = np.zeros_like(x)
        self.v = np.zeros_like(x) + damping
        self.i = 0
        self.D = None

    def __call__(self, g, learning_rate=0.01, b1 = 0.1, b2 = 0.01, lam=1e-4):
        i = self.i
        b1t = 1 - (1-b1)*(lam**i)          # b1t -> 1 over time
        # Update first moment estimate
        ewma(self.m, g, b1t)
        # Update second moment estimate
        ewma(self.v, g*g, b2)
        # Bias correction
        mhat = self.m * (learning_rate / (1-(1-b1)**(i+1)))
        vhat = self.v / (1-(1-b2)**(i+1))
        # Update parameters
        np.sqrt(vhat, out=vhat)
        mhat /= vhat           # inplace

        # this is the analogue of stepsize in adam. this doen't capture the
        # momentum in the numerator
        self.D = learning_rate/vhat

        self.x -= mhat
        self.i += 1
