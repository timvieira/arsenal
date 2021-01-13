class AbstractIntegerizer:

    def __getitem__(self, i):
        if isinstance(i, list):
            return [self._list[ii] for ii in i]
        return self._list[i]

    def __call__(self, k):
        if isinstance(k, list):
            ks = k
            return [self._add(k) for k in ks]
        return self._add(k)

    def _add(self, k):
        raise NotImplementedError()

    # method aliases
    encode = __call__
    decode = __getitem__
    lookup = __getitem__
    add = __call__


class Integerizer(AbstractIntegerizer):
    """
    Class for maintaining a perfect hash for a set of keys.

    >>> a = Integerizer()
    >>> a(list('abcd'))
    [0, 1, 2, 3]

    >>> a(list('ace'))
    [0, 2, 4]

    >>> a[list(range(4))]
    ['a', 'b', 'c', 'd']

    >>> a.freeze()
    >>> a.add('z')
    Traceback (most recent call last):
      ...
    ValueError: Alphabet is frozen. Key "z" not found.

    >>> list(a)
    ['a', 'b', 'c', 'd', 'e']

    """

    def __init__(self, data=None):
        self._map = {}       # str -> int
        self._list = []      # int -> str
        self._frozen = False
        if data: self.add(data)

    def _add(self, k):
        try:
            return self._map[k]
        except KeyError:
            #if not isinstance(k, basestring):
            #    raise ValueError("Invalid key (%s): only strings allowed." % (k,))
            if self._frozen:
                raise ValueError('Alphabet is frozen. Key "%s" not found.' % (k,))
            x = self._map[k] = len(self._list)
            self._list.append(k)
            return x

    def __contains__(self, k):
        return k in self._map

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._list)

    def __eq__(self, other):
        return self._list == other._list

    def __repr__(self):
        return 'Alphabet(size=%s,frozen=%s)' % (len(self), self._frozen)

    def freeze(self):
        self._frozen = True
        return self

    def keys(self):
        return self._list

    def items(self):
        return self._map.items()


def jenkins32(a):
    assert isinstance(a, int) and a >= 0
    a = (a+0x7ed55d16) + (a<<12)
    a = (a^0xc761c23c) ^ (a>>19)
    a = (a+0x165667b1) + (a<<5)
    a = (a+0xd3a2646c) ^ (a<<9)
    a = (a+0xfd7046c5) + (a<<3)
    a = (a^0xb55a4f09) ^ (a>>16)
    return a


# TODO: might be good to write in Cython and provide a few fast hash functions
# for strings, ints, and tuples.
#   ^ I have a reasonable implementation in dyna.learn.features
class FeatureHashing(AbstractIntegerizer):
    """
    >>> h = FeatureHashing(jenkins32, 8)
    >>> h([1, 2, 3])
    [182, 76, 156]

    """

    def __init__(self, h, bits):
        self.h = h
        self.bits = bits
        self.D = 2**bits
        self.mask = self.D - 1   # use bit mask rather than mod for efficiency

    def _add(self, k):
        h = self.h(k)
        assert h >= 0
        return h & self.mask


if __name__ == '__main__':
    import doctest
    doctest.testmod()
