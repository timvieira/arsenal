from arsenal.iterview import iterview


def test_list_iteration():
    """iterview over a list yields every element."""
    items = list(range(50))
    result = list(iterview(items, show=False))
    assert result == items


def test_generator_with_length():
    """iterview over a generator works when length is provided."""
    result = list(iterview((x for x in range(10)), length=10, show=False))
    assert result == list(range(10))


def test_early_break():
    """Breaking out of iterview early yields the expected prefix."""
    result = []
    for i in iterview(range(100), show=False):
        if i == 5:
            break
        result.append(i)
    assert result == [0, 1, 2, 3, 4]


def test_empty():
    """iterview over empty iterable yields nothing."""
    assert list(iterview([], show=False)) == []


def test_transient_mode():
    """Transient mode runs without error."""
    result = list(iterview(range(10), transient=True, show=False))
    assert result == list(range(10))
