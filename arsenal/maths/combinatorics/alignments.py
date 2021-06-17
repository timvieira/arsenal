"""
Enumerate alignments between two sets
"""

def alignments(x, y):
    "Enumerate alignments between two sets"
    yield from _alignments(x, y, 0, set(range(len(y))), [])


def _alignments(
        x, y,
        cursor: 'cursor into x',
        remaining: 'available indices in y',
        align: 'current alignment prefix'
):
    if len(align) == len(x):
        yield align
        return

    # XXX: Below are some heuristics to short-circuit backtracking sooner.
#    from collections import Counter
#    xx = Counter(x[cursor:])
#    yy = Counter([y[j] for j in remaining])
#    for a in xx:
#        if xx[a] > yy[a]:  # if we don't have enough `a`s in y to cover x, quit now.
#            return

    if cursor >= len(x): return
    if len(remaining) == 0: return
    for j in remaining:
        if x[cursor] == y[j]:
            yield from _alignments(x, y, cursor+1,
                                   remaining - {j},
                                   align + [(cursor,j)])


def check_property(x, y, a):
    for i,j in a:
        assert x[i] == y[j]
        ii, jj = zip(*a)
        # test that `a` is a one-to-one function
        assert len(set(ii)) == len(x) == len(set(jj)) == len(a)
        assert set(ii) == set(range(len(x)))
        assert set(jj) <= set(range(len(y)))


def test():
    from arsenal import ok
    x, y = 'abc', 'xxabcxabcabcaaax'

    aligns = []
    for t, a in enumerate(alignments(x, y)):
        check_property(x, y, a)
        aligns.append(frozenset(a))
    assert len(set(aligns)) == len(aligns)   # check for spurious ambiguity
    assert len(aligns) == 6*3*3

    x, y = 'cba', 'xabcc'
    aligns = []
    for t, a in enumerate(alignments(x, y)):
        check_property(x, y, a)
        aligns.append(frozenset(a))
    assert len(set(aligns)) == len(aligns)   # check for spurious ambiguity
    assert len(aligns) == 2

    print(ok)


if __name__ == '__main__':
    test()
