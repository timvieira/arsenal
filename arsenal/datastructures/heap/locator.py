from arsenal.datastructures.heap import MaxHeap


class LocatorMaxHeap(MaxHeap):
    """
    Dynamic heap. Maintains max of a map, via incrementally maintained partial
    aggregation tree. Also known a priority queue with 'locators'.

    This data structure efficiently maintains maximum of the priorities of a set
    of keys. Priorites may increase or decrease. (Many max-heap implementations
    only allow increasing priority.)

    """

    def __init__(self, **kw):
        super().__init__(**kw)
        self.key = {}   # map from index `i` to `key`
        self.loc = {}   # map from `key` to index in `val`

    def __repr__(self):
        return repr({k: self[k] for k in self.loc})

    def pop(self):
        k,v = self.peek()
        super().pop()
        return k,v

    def peek(self):
        return self.key[1], super().peek()

    def _remove(self, i):
        # update the locator stuff for last -> i
        last = self.val.end - 1
        self.swap(i, last)
        old = self.val.pop()
        # remove the key/loc/val associated with the deleted node.
        self.loc.pop(self.key.pop(last))
        # special handling for when the heap has size one.
        if i == last: return
        self._update(i, old, self.val[i])

    def __contains__(self, k):
        return k in self.loc

    def __getitem__(self, k):
        return self.val[self.loc[k]]

    def __setitem__(self, k, v):
        "upsert (update or insert) value associated with key."
        if k in self:
            # update
            i = self.loc[k]
            super()._update(i, self.val[i], v)
        else:
            # insert (put new element last and bubble up)
            i = self.val.push(v)
            # Annoyingly, we have to write key/loc here the super class's push
            # method doesn't allow us to intervene before the up call.
            self.val[i] = v
            self.loc[k] = i
            self.key[i] = k
            # fix invariants
            self.up(i)

    def swap(self, i, j):
        super().swap(i, j)
        self.key[i], self.key[j] = self.key[j], self.key[i]
        self.loc[self.key[i]] = i
        self.loc[self.key[j]] = j

    def check(self):
        super().check()
        for key in self.loc:
            assert self.key[self.loc[key]] == key
        for i in range(1, self.val.end):
            assert self.loc[self.key[i]] == i
