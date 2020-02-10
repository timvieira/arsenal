from scipy.optimize import minimize


class NProx:
    """
    Numerically estimate the proximal operator `Prox_{s*f}(x)` and related
    concepts such as the Moreau envelope.

    This implementation is not efficient and should only be used for testing
    purposes.

    https://web.stanford.edu/~boyd/papers/pdf/prox_algs.pdf
    """

    def __init__(self, f, s):
        self.f = f
        self.s = s

    def solve(self, x):
        return minimize(lambda z: self.objective(x, z), x)

    def objective(self, x, z):
        d = (x-z)
        return self.f(z) + 0.5/self.s * d @ d

    def op(self, x):
        return self.solve(x).x

    def func(self, x):
        "Proximally smoothed `f` with smoothing parameter `s > 0`."
        return self.solve(x).fun

    def grad(self, x):
        "Gradient of `prox_func` wrt `x`."
        return (x - self.op(x))/self.s
