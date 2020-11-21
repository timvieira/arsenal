import numpy as np
from arsenal.maths.compare import compare
from arsenal.maths.rvs import spherical
from arsenal.iterview import iterview


# cg: Solve a linear systems, A x = b, using only A-x products. Assumes the
# matrix `A` is positive definite (same conditions as conjugate gradient). The
# cg solver requires that the Ax operator is an instance of LinearOperator
from scipy.sparse.linalg import cg as implicit_cg
from scipy.sparse.linalg import LinearOperator


from scipy.optimize import minimize
from scipy.linalg import norm
from arsenal import iterview


def fd_Hessian(f, x, eps=1e-5):
    [d] = x.flatten().shape
    x = x.flat
    [F] = f().shape
    H = np.zeros((d,d,F))
    for i in range(d):
        for j in range(d):
            # central-difference approximation of Hessian

            x_i = x[i]
            x_j = x[j]

            x[i] = x_i + eps
            x[j] = x_j + eps

            bb = f()

            x[i] = x_i + eps
            x[j] = x_j - eps

            ba = f()

            x[i] = x_i - eps
            x[j] = x_j + eps

            ab = f()

            x[i] = x_i - eps
            x[j] = x_j - eps

            aa = f()

            # reset
            x[i] = x_i
            x[j] = x_j

            H[i,j] = (bb - ba - ab + aa) / (4*eps**2)

    return H


def prox_numerical(f, x, s, jac=None):
    "Numerically estimate the proximal operator `Prox_{s*f}(x)`."

    def fg(z):
        d = (z-x)
        p = 0.5/s * (d @ d)
        if jac:
            fz, gz = f(z)
            return (fz + p, gz + 1/s * d)
        else:
            return f(z) + p

    sol = minimize(fg, x, jac=jac)
    for _ in range(4):
        sol = minimize(fg, sol.x, jac=jac)
    return sol


def fd_Jv(f, x, shape=None):
    """Finite-difference approximation to a Jacobian-vector product, J[f](x) v,
    where f: Rⁿ ↦ Rᵐ.

    Example: If f is a gradient, this function approximates Hessian-vector
    products.

    Solve a linear system for second-order gradient methods without
    materializing the Hessian or Fisher matrix. For example, the natural
    gradient direction in an exponential family:

      g = Euclidean_gradient(w)
      Fvp = fd_Jv(dlogZ, w)     # Fisher-vector products
      ng = implicit_cg(Fvp, g)[0]

    """
    if shape is None:
        [N] = x.shape
        [M] = f(x).shape
    else:
        N,M = shape
    def Jv(v, eps=1e-5):
        return (f(x + eps*v) - f(x - eps*v)) / (2*eps)
    return LinearOperator((N, M), matvec=Jv)


def finite_difference(f, eps=1e-5):
    def grad(x):
        x = np.array(x)
        g = []
        for k in range(x.shape[0]):
            v = x[k]
            x[k] = v + eps
            b = f(x)
            x[k] = v - eps
            a = f(x)
            x[k] = v
            g.append((b-a) / 2 / eps)
        return np.array(g)
    return grad


def fdcheck(func, w, g, keys = None, eps = 1e-5, quiet=0, verbose=1, progressbar=1, throw=True):
    """
    Finite-difference check.

    Returns `arsenal.math.compare` instance.

    - `func`: zero argument function, which references `w` in caller's scope.
    - `w`: parameters.
    - `g`: gradient estimate to compare against
    - `keys`: dimensions to check
    - `eps`: perturbation size

    """
    if quiet:
        verbose = 0
        progressbar = 0

    if keys is None:
        if hasattr(w, 'keys'):  # support for sparse vectors represented as a dictionary-like object.
            keys = list(w.keys())
            d = {}
        else:
            # use flat views, if need be.
            if len(w.shape) > 1: w = w.flat
            if len(g.shape) > 1: g = g.flat
            d = np.zeros_like(w)
            keys = list(range(len(w)))    # TODO: these keys have lost their names. So not good for debugging.
    else:
        d = {}

    for k in (iterview(keys) if progressbar else keys):
        was = w[k]
        w[k] = was + eps
        b = func()
        w[k] = was - eps
        a = func()
        w[k] = was
        d[k] = (b-a) / (2*eps)

    if throw and not np.allclose([d[k] for k in keys],
                                 [g[k] for k in keys]):
        compare(d, g, verbose=True)
        raise AssertionError('^^^^ see compare above')


    return compare([d[k] for k in keys],
                   [g[k] for k in keys],
                   verbose=verbose)


def quick_fdcheck(func, w, g, n_checks = 20, eps = 1e-5,
                  quiet=True, verbose=False, progressbar=False, throw=True):
    """
    Check gradient along random directions (a faster alternative to axis-aligned directions).

    Tim Vieira (2017) "How to test gradient implementations"
    https://timvieira.github.io/blog/post/2017/04/21/how-to-test-gradient-implementations/

    """

    if quiet:
        verbose = 0
        progressbar = 0

    keys = ['rand_%s' % i for i in range(n_checks)]
    H = {}
    G = {}

    was = w.flatten()

    w = np.asarray(w.flat)
    g = np.asarray(g.flat)

    dim = len(w)

    for k in (iterview(keys) if progressbar else keys):
        d = spherical(dim)
        G[k] = g.dot(d)
        w[:] = was + eps*d
        b = func()
        w[:] = was - eps*d
        a = func()
        w[:] = was
        H[k] = (b-a) / (2*eps)

    different = not np.allclose(list(H.values()), list(G.values()))
    if verbose or different:
        compare(H, G, verbose=True)

    if different and throw:
        raise AssertionError('^^^^ see compare above')

    return compare(H, G, verbose=False)
