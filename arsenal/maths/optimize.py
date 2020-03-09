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

    def solve(self, x, y0=None):
        return minimize(lambda y: self.objective(x, y), y0 if y0 is not None else x)

    def objective(self, x, y):
        d = (x - y)
        return self.f(y) + 0.5/self.s * d @ d

    def op(self, x, **kw):
        return self.solve(x, **kw).x

    def func(self, x, **kw):
        "Proximally smoothed `f` with smoothing parameter `s > 0`."
        return self.solve(x, **kw).fun

    def grad_like(self, x, **kw):
        "Gradient of `prox_func` wrt `x`."
        return (x - self.op(x, **kw)) / self.s


class NProj:

    def __init__(self, C, type):
        self.C = C
        self.type = type
        self.constraints = [{
            'fun': self.C,
            'type': {'>=': 'ineq', '==': 'eq'}[self.type],
        }]

    def solve(self, x, y0=None):
        sol = minimize(
            lambda y: 0.5 * (y - x) @ (y - x),
            y0 if y0 is not None else x,
            constraints = self.constraints,
        )
        if not sol.success: print(sol.message)
        return sol

    def op(self, x, **kw):
        return self.solve(x, **kw).x

    def func(self, x, **kw):
        return self.solve(x, **kw).fun

    def grad_like(self, x, **kw):
        "Gradient of `prox_func` wrt `x`."
        return (x - self.op(x, **kw))


def is_subgradient(f, g, x):
    "Numerically check whether or not `g` is a subgradient of `f` at `x`."
    # Check the condition:
    #    for all y, f(y) - f(x) >= g @ (y - x).
    # iff
    #    for all y, f(y) - g @ y >= f(x) - g @ x
    #         min_y f(y) - g @ y >= f(x) - g @ x
    sol = minimize(lambda y: f(y) - g @ y, x)
    return sol.fun >= f(x) - g @ x
