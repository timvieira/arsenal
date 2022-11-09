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



def test_f1():

    if 0:
        def f1(correct, predict, n_labels):
            assert correct.shape == predict.shape
            tp, fp, fn = np.zeros((3, n_labels))
            for (c, p) in zip(correct, predict):
                if c == p:
                    tp[c] += 1
                else:
                    fp[p] += 1
                    fn[c] += 1
            F,P,R = np.zeros((3, n_labels))
            for c in range(n_labels):
                if tp[c] > 0:
                    P[c] = tp[c] / (tp[c] + fp[c])
                    R[c] = tp[c] / (tp[c] + fn[c])
                    F[c] = 2*P[c]*R[c] / (P[c] + R[c])
            return F,P,R

        def test_statistic(predict):
            f,_,_ = f1(c, predict, 2)
            return f[1]   # F1-measure for label 1.
    else:
        # accuracy
        def test_statistic(predict): return np.mean(c == predict)

    t = 0.05
    c = np.array([0,1,0,1,0,1,0,1,0,1,0,1])   # correct labels
    a = np.array([1,1,1,1,0,1,1,0,1,1,0,0])
    b = np.array([0,1,0,1,0,1,0,1,0,1,0,1])
    paired_permutation_test(a, b, statistic=test_statistic,
                            threshold=t, verbose=True)


if __name__ == '__main__':
    test_f1()
