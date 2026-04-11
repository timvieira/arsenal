import numpy as np

from arsenal.maths.stats.permutation_test import verbose_paired_perm_test


def test_paired_perm():
    xs = np.array([1, 2, 3, 4, 5, 6])
    # system that is consistently +1 should be significant
    p = verbose_paired_perm_test(xs + 1, xs)
    assert p < 0.05
    # same system should not be significant
    p = verbose_paired_perm_test(xs, xs)
    assert p > 0.05
