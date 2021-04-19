import numpy as np
from scipy.linalg import inv, det
from scipy.linalg.blas import dger


class Inv:

    def __init__(self, A):
        B = np.array(inv(A), order='F', copy=True)
        assert B.flags['F_CONTIGUOUS']
        self.B = B

    def rank_one_update(self, u, v):
        # https://timvieira.github.io/blog/post/2021/03/25/fast-rank-one-updates-to-matrix-inverse/
        B = self.B
        Bu = B @ u
        s = 1 + float(v.T @ Bu)
        alpha = -1 / s
        # Warning: `overwrite_a=True` silently fails when B is not an order=F array!
        dger(alpha, Bu, v.T @ B, a=B, overwrite_a=1)
        return s

    @property
    def value(self):
        return self.B


class InvAndDet(Inv):

    def __init__(self, A):
        super().__init__(A)
        self.D = det(A)

    def rank_one_update(self, u, v):
        s = super().rank_one_update(u, v)
        self.D *= s


def test():

    n = 10

    A = np.random.randn(n,n)
    B = inv(A)
    u = np.random.randn(n,1)
    v = np.random.randn(n,1)

    B = InvAndDet(A)

    B.rank_one_update(u,v)
    assert np.allclose(inv(A + np.outer(u, v)), B.value)

    print(det(A + np.outer(u, v)), B.D)
    assert np.allclose(det(A + np.outer(u, v)), B.D)

    print('ok')


if __name__ == '__main__':
    test()
