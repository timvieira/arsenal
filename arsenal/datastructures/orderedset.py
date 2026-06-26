"""
OrderedSet -- a set which remembers insertion order.
"""
from itertools import islice


class OrderedSet:
    """
    Set which remembers insertion ordering. Iteration is stable across
    additions and removals.
    """
    __slots__ = ('_d',)
    def __init__(self, elems=None):
        self._d = {}
        if elems is not None:
            for x in elems:
                self._d[x] = None
    def __contains__(self, item):
        return item in self._d
    def __iter__(self):
        return iter(self._d)
    def add(self, item):
        self._d[item] = None
    def __len__(self):
        return len(self._d)
    def __repr__(self):
        return 'OrderedSet(%r)' % list(self._d)
    def __getitem__(self, key):
        if isinstance(key, slice):
            return list(self._d)[key]
        if key < 0:
            return list(self._d)[key]
        try:
            return next(islice(self._d, key, key + 1))
        except StopIteration:
            raise IndexError('OrderedSet index out of range')
    def __sub__(self, other):
        new = OrderedSet()
        for x in self:
            if x not in other:
                new.add(x)
        return new
    def __or__(self, other):
        new = OrderedSet()
        for x in self:
            new.add(x)
        for x in other:
            new.add(x)
        return new
    def __ior__(self, other):
        for x in other:
            self.add(x)
        return self
    def isdisjoint(self, other):
        return self._d.keys().isdisjoint(other._d.keys() if isinstance(other, OrderedSet) else other)
    def __lt__(self, other):
        return self._d.keys() < (other._d.keys() if isinstance(other, OrderedSet) else other)
    def __le__(self, other):
        return self._d.keys() <= (other._d.keys() if isinstance(other, OrderedSet) else other)
    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return self._d.keys() == other._d.keys()
        elif isinstance(other, set):
            return set(self._d) == other
        else:
            return False
    def remove(self, x):
        del self._d[x]
