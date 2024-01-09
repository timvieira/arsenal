class pdict(dict):

    def __init__(self):
        """
        Initialize pdict by creating binary heap of pairs (value,key).
        Note that changing or removing a dict entry will
        not remove the old pair from the heap until it is found by peek() or
        until the heap is rebuilt.'
        """
        self.__heap = []
        dict.__init__(self)

    def pop(self):
        x = self.peek()
        del self[x]
        return x

    def peek(self):
        "Find smallest item after removing deleted items from heap."
        if len(self) == 0: raise IndexError("smallest of empty pdict")
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and heap[smallChild][0] > heap[smallChild+1][0]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem[0] <= heap[smallChild][0]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]

    def __setitem__(self, key, val):
        """
        Change value stored in dictionary and add corresponding
        pair to heap.  Rebuilds the heap if the number of deleted items grows
        too large, to avoid memory leakage.
        """
        dict.__setitem__(self, key, val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.items()]
            self.__heap.sort(key=lambda x: x[0])  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and newPair[0] < heap[(insertionPoint-1)//2][0]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair

    def setdefault(self, key, val):
        "Reimplement setdefault to call our customized __setitem__."
        if key not in self: self[key] = val
        return self[key]
