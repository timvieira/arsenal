class Alphabet(object):
    """
    Bijective mapping from strings to integers.

    >>> a = Alphabet()
    >>> [a[x] for x in 'abcd']
    [0, 1, 2, 3]
    >>> map(a.lookup, range(4))
    ['a', 'b', 'c', 'd']

    >>> a.stop_growth()
    >>> a['e']

    >>> a.freeze()
    >>> a.add('z')
    Traceback (most recent call last):
      ...
    ValueError: Alphabet is frozen. Key "z" not found.

    >>> print a.plaintext()
    a
    b
    c
    d
    """

    def __init__(self):
        self._mapping = {}   # str -> int
        self._flip = {}      # int -> str; timv: consider using array or list
        self._i = 0
        self._frozen = False
        self._growing = True

    def __repr__(self):
        return 'Alphabet(size=%s,frozen=%s)' % (len(self), self._frozen)

    def freeze(self):
        self._frozen = True

    def stop_growth(self):
        self._growing = False

    @classmethod
    def from_iterable(cls, s):
        inst = cls()
        for x in s:
            inst.add(x)
        inst.freeze()
        return inst

    def keys(self):
        return self._mapping.iterkeys()

    def imap(self, seq, emit_none=False):
        """
        Apply alphabet to sequence while filtering. By default, `None` is not
        emitted, so the Note that the output sequence may have fewer items.
        """
        if emit_none:
            for s in seq:
                yield self[s]
        else:
            for s in seq:
                x = self[s]
                if x is not None:
                    yield x

    def map(self, seq, *args, **kwargs):
        return list(self.imap(seq, *args, **kwargs))

    def add_many(self, x):
        for k in x:
            self.add(k)

    def lookup(self, i):
        if i is None:
            return None
#        assert isinstance(i, int)
        return self._flip[i]

    def lookup_many(self, x):
        for k in x:
            yield self.lookup(k)

    def __contains__(self, k):
        assert isinstance(k, basestring)
        return k in self._mapping

    def __getitem__(self, k):
        try:
            return self._mapping[k]
        except KeyError:
            if not isinstance(k, basestring):
                raise ValueError("Invalid key (%s): only strings allowed." % (k,))
            if self._frozen:
                raise ValueError('Alphabet is frozen. Key "%s" not found.' % (k,))
            if not self._growing:
                return None
            x = self._mapping[k] = self._i
            self._flip[x] = k
            self._i += 1
            return x

    add = __getitem__

    def __iter__(self):
        for i in xrange(len(self)):
            yield self._flip[i]

    def enum(self):
        for i in xrange(len(self)):
            yield (i, self._flip[i])

    def __len__(self):
        return len(self._mapping)

    def plaintext(self):
        return '\n'.join(self)

    @classmethod
    def load(cls, filename):
        with file(filename) as f:
            return cls.from_iterable(l.strip() for l in f)

    def save(self, filename):
        with file(filename, 'wb') as f:
            f.write(self.plaintext())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
