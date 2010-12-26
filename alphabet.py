

class Alphabet(object):
    """
    Bijective mapping from strings to integers.

    >>> a = Alphabet()
    >>> [a[x] for x in 'abcdefg']
    [0, 1, 2, 3, 4, 5, 6]
    >>> map(a.lookup, range(7))
    ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    >>> a.stop_growth()
    >>> a['A']

    >>> a.freeze()
    >>> a.add('z')
    Traceback (most recent call last):
      ...
    ValueError: Alphabet is frozen. Key "z" not found.

    """

    def __init__(self):
        self.mapping = {}
        self.flip = {}
        self.i = 0
        self.frozen = False
        self.growing = True

    def freeze(self):
        self.frozen = True

    def stop_growth(self):
        self.growing = False

    @classmethod
    def from_iterable(cls, it):
        inst = cls()
        for x in it:
            inst.add(x)
        inst.freeze()
        return inst

    def lookup(self, i):
        assert isinstance(i, int)
        return self.flip[i]

    def map(self, seq):
        """ apply alphabet to sequence """
        for s in seq:
            x = self[s]
            if x is not None:
                yield x

    def __getitem__(self, k):
        try:
            return self.mapping[k]
        except KeyError:
            if not isinstance(k, basestring):
                raise ValueError("Invalid key (%s): only strings allowed." % k)
            if self.frozen:
                raise ValueError('Alphabet is frozen. Key "%s" not found.' % k)
            if not self.growing:
                return None
            x = self.mapping[k] = self.i
            self.flip[x] = k
            self.i += 1
            return x

    add = __getitem__

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def plaintext(self):
        return '\n'.join(self.lookup(i) for i in xrange(self.i))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
