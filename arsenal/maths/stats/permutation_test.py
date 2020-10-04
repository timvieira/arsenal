import numpy as np


def mc_perm_test(xs, ys, nmc):
    n, k = len(xs), 0.0
    diff = np.abs(np.mean(xs) - np.mean(ys))
    zs = np.concatenate([xs, ys])
    for _ in range(nmc):
        np.random.shuffle(zs)
        k += diff <= np.abs(np.mean(zs[:n]) - np.mean(zs[n:]))
    return k * 1.0 / nmc


def mc_paired_perm_test(xs, ys, nmc):
    """Paired permutation test

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
    n, k = len(xs), 0.0
    zs = xs - ys
    diff = np.abs(np.mean(zs))
    for _ in range(nmc):
        signs = np.random.randint(0,2,n) * 2 - 1
        k += diff <= np.abs(np.mean(signs * zs))
    return k / nmc


def verbose_paired_perm_test(xs, ys, nmc=1000, threshold=0.05, fmt='%.4f'):
    "Let xs be the system you want be greater."
    from arsenal.terminal import colors

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

    print('[paired perm] %s (p=%s)' % (c % 'X (%s) %s Y (%s)' % (fmt % mx,
                                                                 d,
                                                                 fmt % my),
                                       fmt % p))


if __name__ == '__main__':
    def test():
        xs = np.array([1,2,3,4,5,6])
        verbose_paired_perm_test(xs+1, xs)
        verbose_paired_perm_test(xs, xs+1)
        verbose_paired_perm_test(xs, xs)
    test()
