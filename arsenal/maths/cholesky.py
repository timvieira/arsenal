"""
Utilities for working with the Cholesky factorization of a positive-definite matrix.
"""
import numpy as np
import scipy.linalg as la
#import numpy.linalg as la
from arsenal.maths import blocks, random_psd


class Cholesky:
    """Interface to Cholesky factorization of a matrix, which supports updates
    (growing and rank-one updates) as well as efficient utility methods (e.g.,
    solve, det).

    Remarks:

     - We store the factorization (`self.L`) as upper triangular to be
       consistent with `scipy.linalg.cholesky`.  Note that
       `numpy.linalg.cholesky` is lower triangular for some reason.

    """

    def __init__(self, M):
        self.L = la.cholesky(M)

    def update_rank_one(self, x, x_copy=True):
        """
        Rank-one update: compute Chol(M + x xᵀ) given L = Chol(M).

        Remarks:
         - Update is performed in-place (so `self.L` is mutated).
         - We don't need to know `M` to peform the update.
        """
        if x_copy: x = x.copy()
        L = self.L.T
        [n] = x.shape
        assert L.shape == (n,n)
        for k in range(n):
            r = np.hypot(L[k, k], x[k])      #r = np.sqrt(L[k, k]**2 + x[k]**2)
            c = r / L[k, k]
            s = x[k] / L[k, k]
            L[k, k]    = r
            L[k+1:, k] = (L[k+1:n, k] + s * x[k+1:n]) / c
            x[k+1:]    = c * x[k+1:n] - s * L[k+1:n, k]

    def downdate_rank_one(self, z):
        """
        Rank-one down-date: compute Chol(M - x xᵀ) given L = Chol(M).
        """
        # based on https://github.com/scipy/scipy/issues/8188
        L = self.L
        n = L.shape[0]
        eps = n * np.spacing(1.)  # For complex this needs modification
        alpha, beta = np.empty_like(z), np.empty_like(z)
        alpha[-1], beta[-1] = 1., 1.

        for r in range(n):
            a = z[r] / L[r, r]
            alpha[r] = alpha[r-1] - a ** 2
            # Numerically zero or negative
            if alpha[r] < eps:
                # Made up err msg.
                raise la.LinAlgError('The Cholesky factor becomes nonpositive'
                                     'with this downdate at the step {}'.format(r))
            beta[r] = np.sqrt(alpha[r])
            z[r+1:] -= a * L[r, r+1:]
            L[r, r:] *= beta[r] / beta[r-1]
            L[r, r+1:] -= a/(beta[r] * beta[r-1]) * z[r+1:]

    def update_grow(self, B, D):
        """
        Growth update: compute `Chol([[  A, B], [B.T, D]])` given `L = Chol(A)`

        Remarks:
         - We don't need to know `A` to peform the update.

        """
        # TODO: amortize the cost of growing the matrix by using a doubling strategy?
        L = self.L
        [n, m] = B.shape
        assert L.shape == (n,n) and B.shape == (n, m) and D.shape == (m, m)
        B1 = la.solve_triangular(L, B, trans=True)
        C1 = la.cholesky(D - B1.T @ B1)
        L1 = np.block([[L,                B1],
                       [np.zeros((m, n)), C1]])
        self.L = L1

    def solve(self, b):
        return la.cho_solve((self.L, False), b)

    def det(self):
        return np.prod(np.diag(self.L))**2


def test_grow():

    n = 9
    m = 4

    X = random_psd(n)

    [A,B], [C,D] = blocks(X, n-m)
    assert np.allclose(A, A.T)
    assert np.allclose(B, C.T)
    assert np.allclose(D, D.T)

    L = Cholesky(A)
    L.update_grow(B, D)

    assert np.allclose(la.cholesky(X), L.L)
    print('[test grow] pass!')


def test_rank_one():
    n = 10

    A = random_psd(n)
    x = np.random.randn(n)

    L = Cholesky(A)
    L.update_rank_one(x)
    assert np.allclose(L.L, la.cholesky(A + np.outer(x, x)))

    L.downdate_rank_one(x)
    assert np.allclose(L.L, la.cholesky(A))

    print('[test rank-one] pass!')


def test_util():
    n = 10
    X = random_psd(n)

    L = Cholesky(X)
    assert np.allclose(L.det(), np.linalg.det(X))

    # use Cholesky factorization to solve a linear system in O(n^2)
    b = np.random.randn(n)
    assert np.allclose(L.solve(b), la.solve(X, b))

    print('[test util] pass!')


if __name__ == '__main__':
    test_rank_one()
    test_grow()
    test_util()
