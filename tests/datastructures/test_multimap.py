from arsenal.assertions import assert_throws
from arsenal.datastructures.multimap import MultiMap


def test_multimap_basics():
    m = MultiMap()
    m["a","b","c"] = 10
    m["a","b'","c"] = 12

    m["a","b","d"] = 13
    m["a", 14,frozenset(),None,()] = 13   # ragged dimensions allowed

    with assert_throws(AssertionError):
        m["a",:,"d"] = 13
    with assert_throws(AssertionError):
        print(m["a",:10,"d"])

    assert m["a",:,"c"] == MultiMap({('a', 'b', 'c'): 10, ('a', "b'", 'c'): 12})
    assert m[:,:,"d"] == MultiMap({('a', 'b', 'd'): 13})

    # Annoying corner cases for when we don't pass a tuple to get/set items
    m = MultiMap()
    m[1] = 2
    assert m[1,] == m[1] == m
    m[1,] = 2
    assert m[1,] == m[1] == m

    assert list(m) == [(1,)]
