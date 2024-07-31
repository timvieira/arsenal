"""
OrderedSet -- a set which remembers insertion order.
"""

class OrderedSet:
    """
    Set which remembers insertion ordering allowed iteration while changing size
    and determinism.
    """
    __slots__ = 'set', 'list'
    def __init__(self, elems=None):
        self.set = set()
        self.list = []
        if elems is not None:
            for x in elems:
                self.add(x)
    def __contains__(self, item):
        return item in self.set
    def __iter__(self):
        return iter(self.list)
    def add(self, item):
        if item not in self.set:
            self.set.add(item)
            self.list.append(item)
    def __len__(self):
        return len(self.set)
    def __repr__(self):
        return 'OrderedSet(%r)' % self.list
    def __getitem__(self, *args):
        return self.list.__getitem__(*args)
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
        return self.set.isdisjoint(other.set)
    def __lt__(self, other):
        return self.set < other.set
    def __le__(self, other):
        return self.set <= other.set
    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return self.set == other.set
        elif isinstance(other, set):
            return self.set == other
        else:
            return False
    def remove(self, x):
        "this method is slow; avoid"
        self.set.remove(x)
        self.list = [y for y in self.list if x != y]
