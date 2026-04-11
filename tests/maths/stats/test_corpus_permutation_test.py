import numpy as np

from arsenal.maths.stats.corpus_permutation_test import paired_permutation_test


def test_paired_permutation():
    def test_statistic(predict): return np.mean(c == predict)

    t = 0.05
    c = np.array([0,1,0,1,0,1,0,1,0,1,0,1])   # correct labels
    a = np.array([1,1,1,1,0,1,1,0,1,1,0,0])
    b = np.array([0,1,0,1,0,1,0,1,0,1,0,1])
    paired_permutation_test(a, b, statistic=test_statistic,
                            threshold=t, verbose=False)
