class OrderedSet(object):
    """
    Set which remembers insertion ordering allowed iteration while changing size
    and determinism.
    """
    __slots__ = 'set', 'list'
    def __init__(self):
        self.set = set()
        self.list = []
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
