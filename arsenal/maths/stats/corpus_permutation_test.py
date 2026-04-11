"""
Paired permutation test for corpus statistics (non-additive).
"""
import numpy as np
from arsenal.iterview import iterview
from arsenal import colors


def paired_permutation_test(xs, ys, statistic, threshold=0.05, R=10_000, verbose=1):
    "Pair permutation test"

    def effect(xs,ys): return np.abs(statistic(xs) - statistic(ys))   # two-sided: A != B

    ra = statistic(xs)
    rb = statistic(ys)
    diff = effect(xs,ys)       # observed difference

    n = len(xs)
    k = 0
    reps = range(R)
    if verbose: reps = iterview(reps, msg='perm test')
    for _ in reps:
        # randomly generate a vector of zeros and ones (uniformly).
        swaps = np.random.randint(0,2,n).astype(bool)          # flip n coins
        k += diff <= effect(np.select([swaps,~swaps],[xs,ys]), # swap elements accordingly
                            np.select([~swaps,swaps],[xs,ys]))

    s = k/R

    #threshold = 0.5*threshold
    #s *= 0.5   # because we have a two-sided test.

    if verbose:
        # which system has higher reward? is it significant?
        asig = (colors.red % colors.bold) if ra > rb and s <= threshold else '%s'
        bsig = (colors.blue % colors.bold) if rb > ra and s <= threshold else '%s'
        any_sig = colors.bold if s <= threshold else colors.yellow

        print(asig % f'R(A) = {ra:g}')
        print(bsig % f'R(B) = {rb:g}')
        print(any_sig % f'confidence = {(1-s)}\n')

    if s <= threshold:
        return s, -1 if ra > rb else +1
    else:
        return s, 0   # "statistical tie"

