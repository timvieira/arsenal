import random

import numpy as np
from numpy import array, multiply

from arsenal.maths.util import (
    entropy, d_entropy, kl_divergence, cross_entropy,
    normalize, mutual_information, softmax, d_softmax,
    relative_difference, restore_random_state, assert_equal,
)


def test_entropy():
    assert entropy(array((0.5, 0.5))) == 1.0
    assert abs(entropy(array((0.75, 0.25))) - 0.8112781244) < 1e-10
    assert abs(entropy(array((0.1, 0.1, 0.8))) - 0.9219280948) < 1e-10


def test_kl_divergence():
    assert kl_divergence(array((0.5, 0.5)), array((0.5, 0.5))) == 0.0

    # KL, Entropy, and Cross Entropy relationship
    p = array([0.5, 0.5])
    q = array([0.4, 0.6])
    assert_equal(cross_entropy(p, q), (entropy(p) + kl_divergence(p, q)))


def test_normalize():
    assert_equal(array([0.5, 0.5]), normalize(array([2, 2])))


def test_mutual_information():
    Pjoint = normalize(np.random.rand(4, 10))
    assert_equal(mutual_information(Pjoint),
                 mutual_information(Pjoint.T))

    def mi_independent_is_zero(px, py):
        assert mutual_information(multiply.outer(px, py)) <= 1e-10

    p = array([0.5, 0.5])
    q = array([0.4, 0.6])
    mi_independent_is_zero(p, q)
    mi_independent_is_zero(array([0.1, 0.1, 0.2, 0.6]),   # non-square joint
                           array([0.9, 0.1]))


def test_restore_random_state():
    def foo():
        return [(random.randint(0, 100),
                 np.random.randint(0, 100))
                for _ in range(10)]

    with restore_random_state():
        a = foo()
    b = foo()
    assert a == b


def test_softmax_grad():
    from arsenal.maths.checkgrad import fdcheck
    n = 20
    adj = np.random.uniform(-1, 1, size=n)
    x = np.random.uniform(-1, 1, size=n)
    out = softmax(x)
    g = d_softmax(out, x, adj)
    fdcheck(lambda: softmax(x).dot(adj), x, g)


def test_entropy_grad():
    from arsenal.maths import random_dist, fdcheck
    p = random_dist(30)
    fdcheck(lambda: entropy(p), p, d_entropy(p), throw=False)


def test_relative_difference():
    assert relative_difference(np.inf, np.inf) == 0.0
