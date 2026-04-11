import numpy as np
from scipy.linalg import inv, det

from arsenal.maths.inv import InvAndDet


def test_inv_rank_one_update():
    n = 10

    A = np.random.randn(n, n)
    u = np.random.randn(n, 1)
    v = np.random.randn(n, 1)

    B = InvAndDet(A)
    B.rank_one_update(u, v)
    assert np.allclose(inv(A + np.outer(u, v)), B.value)
    assert np.allclose(det(A + np.outer(u, v)), B.D)
