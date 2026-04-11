import numpy as np
import scipy.linalg as la

from arsenal.maths import blocks, random_psd
from arsenal.maths.cholesky import Cholesky


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


def test_rank_one():
    n = 10

    A = random_psd(n)
    x = np.random.randn(n)

    L = Cholesky(A)
    L.update_rank_one(x)
    assert np.allclose(L.L, la.cholesky(A + np.outer(x, x)))

    L.downdate_rank_one(x)
    assert np.allclose(L.L, la.cholesky(A))


def test_util():
    n = 10
    X = random_psd(n)

    L = Cholesky(X)
    assert np.allclose(L.det(), np.linalg.det(X))

    # use Cholesky factorization to solve a linear system in O(n^2)
    b = np.random.randn(n)
    assert np.allclose(L.solve(b), la.solve(X, b))
