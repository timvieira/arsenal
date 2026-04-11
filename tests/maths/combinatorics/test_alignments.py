from arsenal.maths.combinatorics.alignments import alignments, check_property


def test_alignments():
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
