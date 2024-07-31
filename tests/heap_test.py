import numpy as np
from random import random, choice
from arsenal.datastructures.heap import MaxHeap, LocatorMaxHeap, MinMaxHeap, BoundedMaxHeap


class SlowPriorityQueue:
    "Priority queue; Prioritization is based on `__lt__`."
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self.items = {}
    def __iter__(self):
        return iter(self.items)
    def __setitem__(self, k, v):
        self.items[k] = v
        if self.maxsize > 0 and len(self.items) > self.maxsize:
            self.popmin()
        if self.maxsize > 0:
            assert len(self.items) <= self.maxsize
    def popmin(self):
        v,k = min((v, k) for k, v in self.items.items())
        del self.items[k]
        return k, v
    def pop(self):
        v,k = max((v, k) for k, v in self.items.items())
        del self.items[k]
        return k, v
    def __len__(self):
        return len(self.items)


class SlowLocatorHeap:
    "Priority queue; Prioritization is based on `__lt__`."
    def __init__(self):
        self.items = {}
    def __setitem__(self, k, v):
        self.items[k] = v
    def popmin(self):
        v,k = min((v,k) for k,v in self.items.items())
        del self.items[k]
        return k, v
    def popmax(self):
        v,k = max((v,k) for k,v in self.items.items())
        del self.items[k]
        return k, v
    def __len__(self):
        return len(self.items)


def test_basic():
    L = MaxHeap(cap=1)
    S = SlowPriorityQueue()

    for t in range(1000):

        if np.random.uniform(0, 1) < .5:
            v = np.random.uniform(-1, 1)
            L.push(v)
            S[t] = v
            L.check()

        else:
            if L or S:
                v1 = L.pop()
                _, v2 = S.pop()
                assert v1 == v2, [v1, v2]

        L.check()

    print('[basic random workload] pass.')


def test_locator():
    L = LocatorMaxHeap(cap=1)
    S = SlowLocatorHeap()

    K = 1
    for _ in range(1000):

        if np.random.uniform(0, 1) < .5:

            if np.random.uniform(0, 1) < .1:  # new key:
                K += 1
                k = K
            else:
                k = int(np.random.randint(K))

            k = f'mykey[{k}]'

            v = np.random.uniform(-1, 1)
            L[k] = v
            S[k] = v
            L.check()

            #print('upsert', k, v)

        else:

            A = S.items
            B = {k: L[k] for k in L.loc}

            #print('want:', A)
            #if A != B: print('got: ', B)
            assert A == B

            if L or S:
                v2 = S.popmax()
                #print('pop', v2)
                v1 = L.pop()

                assert v1 == v2, [v1, v2]

        L.check()

    print('[locator random workload] pass.')


def test_minmax():
    L = MinMaxHeap(cap=1)
    S = SlowLocatorHeap()

    K = 1
    for _ in range(1000):

        if np.random.uniform(0, 1) < .5:

            if np.random.uniform(0, 1) < .1:  # new key:
                K += 1
                k = K
            else:
                k = int(np.random.randint(K))

            k = f'mykey[{k}]'

            v = np.random.uniform(-1, 1)
            L[k] = v
            S[k] = v

            #print('upsert', k, v)

        else:

            A = S.items
            B = L.map()

            #print('want:', A)
            #if A != B: print('got: ', B)
            assert A == B

            if L or S:

                if np.random.uniform(0, 1) < .5:
                    v2 = S.popmin()
                    v1 = L.popmin()
                else:
                    v2 = S.popmax()
                    v1 = L.popmax()

                assert v1 == v2, [v1, v2]

        L.check()

    print('[min-max random workload] pass.')



def test_bounded():
    maxsize = 5
    L = BoundedMaxHeap(maxsize=maxsize, cap=1)
    S = SlowPriorityQueue(maxsize=maxsize)

    K = 1
    for _ in range(1000):

        if np.random.uniform(0, 1) < .5:

            if np.random.uniform(0, 1) < .1:  # new key:
                K += 1
                k = K
            else:
                k = int(np.random.randint(K))

            k = f'mykey[{k}]'

            v = np.random.uniform(-1, 1)
            L[k] = v
            S[k] = v
            L.check()

            #print('upsert', k, v)

        else:

            A = S.items
            B = L.map()

            #print('want:', A)
            #if A != B: print('got: ', B)
            assert A == B

            if L or S:
                v2 = S.pop()
                v1 = L.pop()
                assert v1 == v2, [v1, v2]

        L.check()

    print('[bounded random workload] pass.')


if __name__ == '__main__':
    from arsenal import testing_framework
    testing_framework(globals())
