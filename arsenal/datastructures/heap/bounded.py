from arsenal.datastructures.heap import LocatorMaxHeap


class MinMaxHeap:

    def __init__(self, **kw):
        self.max = LocatorMaxHeap(**kw)
        self.min = LocatorMaxHeap(**kw)   # will pass negative values here

    def __contains__(self, k):
        return k in self.max
        
    def __setitem__(self, k, v):
        self.max[k] = v
        self.min[k] = -v

    def peekmin(self):
        k, v = self.min.peek()
        return k, -v

    def peekmax(self):
        return self.max.peek()

    def popmax(self):
        k, v = self.max.pop()
        self.min._remove(self.min.loc[k])  # remove it from the min heap
        return k, v

    def popmin(self):
        k, v = self.min.pop()
        self.max._remove(self.max.loc[k])  # remove it from the min heap
        return k, -v

    def check(self):
        self.min.check()
        self.max.check()

    def __len__(self):
        return len(self.max)

    def __repr__(self):
        return repr(self.max)

    def map(self):
        return {k: self.max[k] for k in self.max.loc}


class BoundedMaxHeap(MinMaxHeap):

    def __init__(self, maxsize, **kw):
        super().__init__(**kw)
        self.maxsize = maxsize

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        if len(self) > self.maxsize:
            if v < self.peekmin()[1]:  # smaller than the smallest element.
                return
            else:
                self.popmin()   # evict the smallest element

    def pop(self):
        return self.popmax()

    def check(self):
        super().check()
        assert len(self.max) <= self.maxsize
        assert len(self.min) <= self.maxsize
