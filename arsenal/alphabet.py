class Alphabet(object):
    """
    Class for maintaining a perfect hash for a set of keys.

    >>> a = Alphabet()
    >>> [a[x] for x in 'abcd']
    [0, 1, 2, 3]

    >>> list(map(a.lookup, range(4)))
    ['a', 'b', 'c', 'd']

    >>> a.freeze()
    >>> a.add('z')
    Traceback (most recent call last):
      ...
    ValueError: Alphabet is frozen. Key "z" not found.

    >>> print(a.plaintext())
    a
    b
    c
    d

    >>> print(a)
    Alphabet(size=4,frozen=True)

    >>> list(a)
    ['a', 'b', 'c', 'd']

    >>> a == Alphabet(['a', 'b', 'c', 'd'])
    True

    >>> a == Alphabet(['b', 'a', 'c', 'd'])
    False

    >>> a.map('aabc')
    [0, 0, 1, 2]

    """

    def __init__(self, data=()):
        self._map = {}       # str -> int
        self._list = []      # int -> str
        self._frozen = False
        self.add_many(data)

    def __repr__(self):
        return 'Alphabet(size=%s,frozen=%s)' % (len(self), self._frozen)

    def freeze(self):
        self._frozen = True

#    def keys(self):
#        return self._map.keys()

    def items(self):
        return self._map.items()

    def imap(self, seq):
        """
        Apply alphabet to sequence while filtering. By default, `None` is not
        emitted, so the Note that the output sequence may have fewer items.
        """
        for s in seq:
            yield self[s]

    def map(self, seq):
        return list(self.imap(seq))

    def add_many(self, x):
        for k in x:
            self.add(k)

    def lookup(self, i):
        return self._list[i]

    def lookup_many(self, x):
        return list(map(self.lookup, x))

    def __contains__(self, k):
        return k in self._map

    def __getitem__(self, k):
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

    __call__ = __getitem__
    add = __getitem__

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._map)

    def plaintext(self):
        "assumes keys are strings"
        return '\n'.join(self)

    @classmethod
    def load(cls, filename):
        #if not os.path.exists(filename): return cls()
        with open(filename) as f:
            return cls(l.strip() for l in f)

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.plaintext())

    def __eq__(self, other):
        return self._list == other._list

    encode_many = map
    decode_many = lookup_many

    encode = __getitem__
    decode = lookup


if __name__ == '__main__':
    import doctest
    doctest.testmod()
