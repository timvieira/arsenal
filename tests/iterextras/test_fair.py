from itertools import count

from arsenal.iterextras.fair import fair_product


def test_fair_product():
    # Test that fair_product of two finite iterables gives all pairs
    pairs = list(fair_product(range(3), range(3)))
    assert len(pairs) == 9
    assert set(pairs) == {(i, j) for i in range(3) for j in range(3)}

    # Test that fair_product of infinite iterables yields results
    # and covers the expected pairs within a finite prefix
    seen = set()
    for i, (x, y) in enumerate(fair_product(count(), count())):
        seen.add((x, y))
        if i >= 100:
            break
    # Should have covered (0,0) through several diagonals
    assert (0, 0) in seen
    assert (1, 0) in seen
    assert (0, 1) in seen

    # Test inf-fin
    seen = set()
    for i, (x, y) in enumerate(fair_product(count(), range(3))):
        seen.add((x, y))
        if i >= 20:
            break
    assert (0, 0) in seen
    assert (0, 2) in seen
