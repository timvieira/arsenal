# -*- coding: utf-8 -*-
import numpy as np
from arsenal.math import compare, spherical
from arsenal.iterview import iterview


# cg: Solve a linear systems, A x = b, using only A-x products. Assumes the
# matrix `A` is positive definite (same conditions as conjugate gradient). The
# cg solver requires that the Ax operator is an instance of LinearOperator
from scipy.sparse.linalg import cg as implicit_cg
from scipy.sparse.linalg import LinearOperator


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


# TODO: should probably have one "core" routine for getting the gradient
# estimate that the test routine will use.
def fd(func, w, eps = 1e-5):
    "Compute finite-difference estimate of the gradient of `func` at `w`."
    g = np.zeros_like(w)
    for k in range(len(w)):
        was = w[k]
        w[k] = was + eps
        b = func()
        w[k] = was - eps
        a = func()
        w[k] = was
        g[k] = (b-a) / (2*eps)
    return g


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


def fdcheck(func, w, g, keys = None, eps = 1e-5, quiet=0, verbose=1, progressbar=1):
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
        if hasattr(w, 'keys'):
            keys = w.keys()
            d = {}
        else:
            d = np.zeros_like(w)

            # use flat views, if need be.
            if len(w.shape) > 1:
                w = w.flat
            if len(g.shape) > 1:
                g = g.flat
            if len(d.shape) > 1:
                d = d.flat

            keys = range(len(w))

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

    return compare([d[k] for k in keys],
                   [g[k] for k in keys],
                   verbose=verbose)


def quick_fdcheck(func, w, g, n_checks = 20, eps = 1e-5, verbose=1, progressbar=1):
    "Check gradient along random directions (a faster alternative to axis-aligned directions)."
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

    return compare(H, G, verbose=verbose)


#from arsenal.misc import deprecated
#@deprecated('fdcheck')
def check_gradient(f, grad, theta, alphabet=None, eps=1e-4, tol=0.01, skip_zero=True,
                    verbose=True, progress=True, keys=None, random_subset=None):
    """Check gradient that `f(theta) == grad` by centered-difference approximation.

    Provides feedback on which dimensions differ

    Arguments:

     - `f`: function we are taking the gradient of.

     - `grad`: What we think the gradient is at `theta`.

     - `theta`:

     - `alphabet` (optional): a bijective map from strings to integers. Expects
       `arsenal.alphabet.Alphabet` instance. This is used to map integer-valued
       dimensions to human-readable names (e.g., strings).

     - `eps`: perturbation size

     - `tol`: what is deem an error (we use relative error)

     - `skip_zero`: good relative error is hard to get for values which are
       really small (near zero).

     - `random_subset`: number dimensions to probe in comparison (useful for
       high dimensions because this test is linear in the dimensionality of
       `theta`).

    """

    import numpy as np
    from numpy import zeros_like
    from arsenal.terminal import green, red, yellow
    from random import sample
    from arsenal.math import cosine

    fails = 0

    grad = np.asarray(grad)

    if keys is None:
        if alphabet is not None:
            keys = alphabet._flip.keys()
            assert len(alphabet), 'Alphabet is empty.'
        else:
            keys = range(len(theta))
        if random_subset is not None:
            if hasattr(random_subset, '__iter__'):
                keys = list(random_subset)
            else:
                keys = sample(keys, min(len(keys), random_subset))

    assert len(keys) > 0

    fd = zeros_like(theta)
    for i in (iterview(keys, msg='checkgrad') if progress else keys):
        was = theta[i]
        # perturb right
        theta[i] = was + eps
        right = f(theta)
        # perturb left
        theta[i] = was - eps
        left = f(theta)
        # reset
        theta[i] = was
        # centered difference
        fd[i] = (right - left) / (2*eps)

    w = max(map(len, alphabet.keys())) if alphabet is not None else 0

    nzeros = 0

    for i in keys:
        # check relative error

        if skip_zero and abs(fd[i]) < 1e-10 and abs(grad[i]) < 1e-10:  # both approximately zero
            nzeros += 1
            continue

        relative_error = abs(fd[i] - grad[i]) / max(abs(fd[i]), abs(grad[i]))
        if relative_error > tol:
            name = alphabet.lookup(i) if alphabet is not None else i
            fails += 1

            if verbose:
                print red % 'dim = %s rel-err = %5.3f' % (('%%-%ss' % w) % (name,), relative_error), \
                    'want: %g; got: %g' % (fd[i], grad[i])
            else:
                assert False, \
                    'dim = %s rel-err = %5.3f, want: %g; got: %g' \
                    % (('%%-%ss' % w) % (name,), relative_error, fd[i], grad[i])

    if nzeros * 1.0 / len(keys) >= 0.75:
        print yellow % '[warning] checkgradient skipped a lot of approximately zero components ' \
            'percentage= %g (%s/%s)' % (nzeros * 1.0 / len(keys), nzeros, len(keys))

    if verbose:
        print 'gradient:',
        if not fails:
            print green % 'OK',
        else:
            print red % 'failed %s of %s' % (fails, len(keys)),

        print 'cosine similarity: %g' % cosine(grad[keys], fd[keys])

        # TODO: add sign check.
