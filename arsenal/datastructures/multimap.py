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

