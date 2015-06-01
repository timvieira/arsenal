#!/usr/bin/env python
"""
Find most informative features ranked by information gain (i.e. the ID3 hueristic for decision trees).

Input: a tab-delimited file where each line starts with a label followed by features.
Output: a sorted list of the most informative features.
"""

import sys
from numpy import dot, log, zeros, fromiter, int32
from arsenal.alphabet import Alphabet
from collections import defaultdict


def normalize(p):
    return p / p.sum()


def lidstone(p, delta):
    """
    Lidstone smoothing is a generalization of Laplace smoothing.
    """
    return normalize(p + delta)


def kl_divergence(p, q):
    """ Compute KL divergence of two vectors, K(p || q).
    NOTE: If any value in q is 0.0 then the KL-divergence is infinite.
    """
    return dot(p, log(p) - log(q))


def read_tab_file(f):
    """
    Load really simple tab-separated file format for labeled data. Label is the
    first column, features are the remaining columns.
    """
    for line in f:
        line = line.strip()
        line = line.split('\t')
        if len(line) <= 1:
            continue
        yield line[0], line[1:]


def integerize(data):
    """
    Integerize dataset
    returns a triple (label alphabet, feature alphabet, integerized dataset)
    """
    F = Alphabet()
    L = Alphabet()
    I = [(L[label], fromiter(F.map(features), dtype=int32)) for label, features in data]
    return (L, F, I)



def kl_filter(data,
              verbose=True,
              progress=False,
              out=sys.stdout,
              feature_label_cuttoff=0,
              feature_count_cuttoff=0,
              do_label_count=False):
    """
    data = (label, [features ...])

    KL is a synonym for Information Gain

    KL( p(label) || p(label|feature) )
    """
    (L, F, data) = integerize(data)

    if do_label_count:
        label_count = defaultdict(int)
        for label, _ in data:
            label_count[label] += 1
        label_count = label_count.items()
        label_count.sort(key=lambda x: -x[1])  # sort by count
        print 'label count'
        for k,v in label_count:
            print '%20s => %s' % (k, v)
        sys.exit(0)

    K = len(L)
    M = len(F)

    if progress:
        from arsenal.iterextras import iterview
    else:
        iterview = lambda x, *a, **kw: x

    if progress:
        print >> sys.stderr, '\nTally'

    # label-feature tally (note: we ignore dulicate features)
    counts = zeros((K,M))
    for y, fv in iterview(data):
        counts[y, fv] += 1

    feature_counts = counts.sum(axis=0)

    if feature_count_cuttoff > 0:
        cut = feature_counts < feature_count_cuttoff

        #if verbose:
        print >> sys.stderr, '%s of %s below cutoff of %s' \
            % (cut.sum(), len(feature_counts), feature_count_cuttoff)

        if progress:
            print >> sys.stderr, '%s / %s (%.2f%%) features below cuttoff' % \
                (cut.sum(), M, cut.sum()*100.0/M)

        # zero-out features below cuttoff
        counts[:, cut] = 0

    if feature_label_cuttoff:
        cut = counts < feature_label_cuttoff

        if progress:
            print >> sys.stderr, '%s / %s (%.2f%%) feature-label pairs below cuttoff' % \
                (cut.sum(), K*M, cut.sum()*100.0/(K*M))

        # zero-out features below cuffoff
        counts[cut] = 0

    label_prior = lidstone(counts.sum(axis=1), 0.001)  # avoids divide-by-zero

    # compute KL
    if progress:
        print >> sys.stderr, '\nKL'

    KL = zeros(M)
    for f in iterview(xrange(M)):
        label_given_f = lidstone(counts[:,f], 0.001)   # avoids divide-by-zero
        KL[f] = -kl_divergence(label_prior, label_given_f)

    # print KL-feature, most-informative first
    for i in KL.argsort():

        z = counts[:,i].sum()

        if z == 0:
            continue

        p = counts[:,i] * 1.0 / z

        l = [(v, k) for k,v in zip(L, p) if v > 0]
        l.sort()

        z = (-KL[i], F.lookup(i), l)

        if verbose:
            print >> out, '%8.6f\t%s\t%s' % (-KL[i], int(counts[:,i].sum()), F.lookup(i)), '\t\033[32m', ' '.join('%s(%.4f)' % (k,v) for v, k in l), '\033[0m'

        yield z


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('input', type=file)
    p.add_argument('--feature-cuttoff', type=int, default=0)
    p.add_argument('--feature-label-cuttoff', type=int, default=0)
    p.add_argument('--progress', action='store_true')
    args = p.parse_args()

    #list(kl_filter(read_tab_file(file(sys.argv[1]) if len(sys.argv) == 2 else sys.stdin)))

    for _ in kl_filter(read_tab_file(args.input),
                       feature_count_cuttoff=args.feature_cuttoff,
                       feature_label_cuttoff=args.feature_label_cuttoff,
                       progress=args.progress):
        pass
