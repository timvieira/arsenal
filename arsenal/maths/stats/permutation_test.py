import numpy as np


def mc_perm_test(xs, ys, samples=10000, statistic=np.mean):
    def effect(xs,ys): return np.abs(statistic(xs) - statistic(ys))
    n, k = len(xs), 0.0
    diff = np.abs(np.mean(xs) - np.mean(ys))
    zs = np.concatenate([xs, ys])
    for _ in range(samples):
        np.random.shuffle(zs)
        k += diff <= effect(zs[:n], zs[n:])
    return k / samples


def mc_paired_perm_test(xs, ys, samples=10000, statistic=np.mean):
    """
    Paired permutation test

      >>> xs = np.array([1,2,3,4,5,6])
      >>> ys = np.array([2,3,4,5,6,7])
      >>> u = mc_perm_test(xs, ys, 1000)
      >>> p = mc_paired_perm_test(xs, ys, 1000)

    Under the unpaired test, we do not have a significant difference because the
    systems only differ in two positions.

      >>> assert u > .40

    Under the Paired test, we have more power!
      >>> assert p < .05

    """
    def effect(xs,ys): return np.abs(statistic(xs) - statistic(ys))
    assert len(xs) == len(ys)
    n, k = len(xs), 0
    diff = effect(xs,ys)    # observed difference
    for _ in range(samples):  # for each random sample
        swaps = np.random.randint(0,2,n).astype(bool)     # flip n coins
        k += diff <= effect(np.select([swaps,~swaps],[xs,ys]), # swap elements accordingly
                            np.select([~swaps,swaps],[xs,ys]))
    return k / samples  # fraction of random samples that achieved at least the observed difference


from itertools import product
def bf_paired_perm_test(xs, ys, statistic=np.mean):
    def effect(xs,ys): return np.abs(statistic(xs) - statistic(ys))
    assert len(xs) == len(ys)
    observed = effect(xs, ys)
    p = 0.0; n = len(xs)
    for swaps in product(*([0,1] for _ in range(n))):
        swaps = np.array(swaps, dtype=bool)
        pe = 2**-n
        E = effect(np.select([swaps,~swaps],[xs,ys]), # swap elements accordingly
                   np.select([~swaps,swaps],[xs,ys]))
        p += pe * (E >= observed)
    return p


def verbose_paired_perm_test(xs, ys, nmc=10_000, threshold=0.05, fmt='%.4f'):
    "Let xs be the system you want be greater."
    from arsenal import colors

    p = mc_paired_perm_test(xs, ys, nmc)

    mx = np.mean(xs)
    my = np.mean(ys)
    if p <= threshold:
        if mx > my:
            c = colors.green
            d = '>'
        else:
            c = colors.red
            d = '<'
    else:
        c = colors.yellow
        d = '~'

    #print('brute-force', bf_paired_perm_test(xs, ys))

    print('[paired perm] %s (p=%s)' % (c % 'X (%s) %s Y (%s)' % (fmt % mx,
                                                                 d,
                                                                 fmt % my),
                                       fmt % p))

    return p


if __name__ == '__main__':
    def test():
        xs = np.array([1,2,3,4,5,6])
        verbose_paired_perm_test(xs+1, xs)
        verbose_paired_perm_test(xs, xs+1)
        verbose_paired_perm_test(xs, xs)
    test()
