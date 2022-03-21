class MultiMap:
    """
    Multi-dimensional map data structure.
    """

    def __init__(self, vals=None):
        self.vals = {} if vals is None else vals
        self.index = {}

    def __iter__(self):
        return iter(self.vals)

    def __setitem__(self, item, val):
        if not isinstance(item, (list, tuple)): item = (item,)
        assert not any(isinstance(y, slice) for y in item), 'setting range values not supported'
        if item not in self.vals:
            # We only need to update indexes when we get a new item because
            # indexes only track the support.  To update, we loop through all
            # active indexes (i.e., query patterns).
            for m,ix in self.index.items():
                k = tuple(item[i] for i in m)
                if k not in ix: ix[k] = set()
                ix[k].add(item)
        self.vals[item] = val

    def __getitem__(self, query):
        if not isinstance(query, (list, tuple)): query = (query,)
        for y in query:
            if isinstance(y, slice):
                assert y == slice(None, None, None), 'only simple slices allowed.'
        m = tuple(i for i, y in enumerate(query) if not isinstance(y, slice))
        k = tuple(y for i, y in enumerate(query) if not isinstance(y, slice))
        if m not in self.index: self._index(m)
        return MultiMap({x: self.vals[x] for x in self.index[m].get(k, set())
                         if len(x) == len(query)})

    def _index(self, m):
        self.index[m] = ix = {}
        for x in self.vals:
            k = tuple(x[i] for i in m)
            if k not in ix: ix[k] = set()
            ix[k].add(x)
        return ix

    def __repr__(self):
        return f'MultiMap({self.vals})'

    def __eq__(self, other):
        return self.vals == other.vals

    def __str__(self):
        # Sort if types allow it, otherwise fall back to the order in vals dictionary
        try:
            vs = sorted(self.vals)
        except TypeError:
            vs = self.vals
        return 'MultiMap {\n%s\n}' % '\n'.join(f'  {x}: {self.vals[x]},' for x in vs)


def tests_basics():
    m = MultiMap()
    m["a","b","c"] = 10
    m["a","b'","c"] = 12

    m["a","b","d"] = 13
    m["a", 14,frozenset(),None,()] = 13   # ragged dimensions allowed (YMMV), dims can have mixed types

    from arsenal.assertions import assert_throws
    with assert_throws(AssertionError):
        m["a",:,"d"] = 13
    with assert_throws(AssertionError):
        print(m["a",:10,"d"])

    assert m["a",:,"c"] == MultiMap({('a', 'b', 'c'): 10, ('a', "b'", 'c'): 12})
    assert m[:,:,"d"] == MultiMap({('a', 'b', 'd'): 13})

    print(m)

    # Note: This does not grab prefixes,
    # print(m["a",:,:])

    # Annoying corner cases for when we don't pass a tuple to get/set items
    m = MultiMap()
    m[1] = 2
    assert m[1,] == m[1] == m
    m[1,] = 2
    assert m[1,] == m[1] == m

    assert list(m) == [(1,)]


if __name__ == '__main__':
    tests_basics()
