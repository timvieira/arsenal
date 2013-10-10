import warnings

_NOTFOUND = object()


class Flipdict(dict):
    """An injective (one-to-one) python dict.  Ensures that each key
    maps to a unique value, and each value maps back to that same key.
    Each instance has a "flip" attribute to access the inverse
    mapping.

    A Flipdict is a dict, implementing the dict API (except dict.fromkeys)::
        >>> keys = (1, 2, 3)
        >>> vals = ('one', 'two', 'three')
        >>> fd = Flipdict(zip(keys, vals))
        >>> fd
        Flipdict({1: 'one', 2: 'two', 3: 'three'})
        >>> fd[1]
        'one'
        >>> fd.get(4, 'four')
        'four'

    Each Flipdict has a "flip" attribute, a Flipdict with the inverse mapping::
        >>> fd is fd.flip.flip
        True
        >>> fd.flip['one']
        1
        >>> fd.flip.setdefault('four', 4)
        4
        >>> fd
        Flipdict({1: 'one', 2: 'two', 3: 'three', 4: 'four'})
        >>> fd.flip
        Flipdict({'four': 4, 'one': 1, 'three': 3, 'two': 2})

    NOTE: Remapping a key -- OR A VALUE -- will erase the old mapping.
    This behavior maintains the inverse mapping, but may be
    unexpected.  Check the docstring of Flipdict.__setitem__ for more
    details.  An example::
        >>> fd.flip['one'] = 4  # Erases both (1,'one') and (4,'four') !!
        >>> fd
        Flipdict({2: 'two', 3: 'three', 4: 'one'})
    
    Some other misc. examples::
        >>> del fd.flip.flip.flip['two']
        >>> fd.flip.update({'zero':0, 'zilch':0, 'zip':0}, naught=0)
        >>> fd  # We only expect a single mapping for key=0.
        Flipdict({0: 'naught', 3: 'three', 4: 'one'})
        >>> sorted(fd.flip.items())
        [('naught', 0), ('one', 4), ('three', 3)]
    """

    def __init__(self, *args, **kw):
        """Similar to dict.__init__

        Examples::
            >>> keys = (1, 2, 3)
            >>> vals = ('one', 'two', 'three')
            >>> fd = Flipdict(zip(keys, vals))
            >>> fd == Flipdict({1: 'one', 2: 'two', 3: 'three'})
            True
            >>> fd == Flipdict(one=1, two=2, three=3).flip
            True

        NOTE: If multiple keys map to the same value, then only ONE of
        those (key, value) mappings will be present after the __init__.
        The other (key, value) pairs will have vanished::
            >>> d = dict.fromkeys(range(5), 'value')
            >>> len( Flipdict(d) )
            1
        """
        self._flip = dict.__new__(self.__class__)
        setattr(self._flip, "_flip", self)
        for key, val in dict(*args, **kw).iteritems():
            self[key] = val

    @property
    def flip(self):
        """The inverse mapping.

        Example::
            >>> keys = (1, 2, 3)
            >>> vals = ('one', 'two', 'three')
            >>> fd = Flipdict(zip(keys, vals))
            >>> fd.flip['two']
            2
            >>> fd.flip.flip[2]
            'two'
            >>> fd is fd.flip.flip
            True
            >>> fd.flip is fd.flip.flip.flip
            True
        """
        return self._flip


    #{ Non-mutating methods that are NOT delegated to the dict superclass.

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, dict(self))

    __str__ = __repr__

    def copy(self):
        """Cf. dict.copy"""
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, keys, value=None):
        """Cf. dict.fromkeys

        NOTE: This method is not useful for a Flipdict, because each
        key must map to a UNIQUE value.
        """
        warnings.warn('%s.fromkeys is not useful'
                      ' --- each key must map to a UNIQUE value' % cls.__name__,
                      DeprecationWarning)
        return cls(dict.fromkeys(keys, value))

    #}


    #{ Mutating methods.  These must keep the inverse mapping in sync!

    def __setitem__(self, key, val):
        """Similar to dict.__setitem__

        NOTE: Remapping a key -- OR A VALUE -- will erase the old
        mapping.  This behavior maintains the inverse mapping, but may
        be unexpected::        
            >>> keys = (1, 2, 3)
            >>> vals = ('ant', 'bug', 'cat')
            >>> fd = Flipdict(zip(keys, vals))
            >>> fd
            Flipdict({1: 'ant', 2: 'bug', 3: 'cat'})

            >>> fd.setdefault(4, 'dog')  # Both key and value are new.
            'dog'
            >>> fd[1] = 'ant'            # This mapping already exists.
            >>> fd[1] = 'ape'            # Map an old key to a new value.
            >>> fd                       # No surprises; behaves like a dict.
            Flipdict({1: 'ape', 2: 'bug', 3: 'cat', 4: 'dog'})

            >>> fd['ant'] = 'bug'        # AHA! Map a new key to an old value!
            >>> fd[2]
            Traceback (most recent call last):
                ....
            KeyError: 2
            >>> fd
            Flipdict({'ant': 'bug', 1: 'ape', 3: 'cat', 4: 'dog'})

            >>> oldKey = fd[4]
            >>> oldVal = fd.flip['cat']
            >>> fd.flip['cat'] = 4       # AHA! Re-map with old key AND value!
            >>> oldKey in fd
            False
            >>> oldVal in fd.flip
            False
            >>> fd
            Flipdict({'ant': 'bug', 1: 'ape', 4: 'cat'})
        """
        v = self.get(key, _NOTFOUND)
        k = self._flip.get(val, _NOTFOUND)
        if k is not _NOTFOUND:  dict.__delitem__(self, k)
        if v is not _NOTFOUND:  dict.__delitem__(self._flip, v)
        dict.__setitem__(self,       key, val)
        dict.__setitem__(self._flip, val, key)

    def setdefault(self, key, default = None):
        """Cf. dict.setdefault

        NOTE: Remapping a key -- OR A VALUE -- will erase the old
        mapping.  This behavior maintains the inverse mapping, but may
        be unexpected.  Cf. Flipdict.__setitem__.
        """
        # Copied from python's UserDict.DictMixin code.
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def update(self, other = None, **kwargs):
        """Cf. dict.update

        NOTE: Remapping a key -- OR A VALUE -- will erase the old
        mapping.  This behavior maintains the inverse mapping, but may
        be unexpected.  Cf. Flipdict.__setitem__.
        """
        # Copied from python's UserDict.DictMixin code.
        # Make progressively weaker assumptions about "other"
        if other is None:
            pass
        elif hasattr(other, 'iteritems'):  # iteritems saves memory and lookups
            for k, v in other.iteritems():
                self[k] = v
        elif hasattr(other, 'keys'):
            for k in other.keys():
                self[k] = other[k]
        else:
            for k, v in other:
                self[k] = v
        if kwargs:
            self.update(kwargs)

    def __delitem__(self, key):
        val = dict.pop(self, key)
        dict.__delitem__(self._flip, val)

    def pop(self, key, *args):
        """Cf. dict.pop"""
        val = dict.pop(self, key, *args)
        dict.__delitem__(self._flip, val)
        return val

    def popitem(self):
        """Cf. dict.popitem"""
        key, val = dict.popitem(self)
        dict.__delitem__(self._flip, val)
        return key, val

    def clear(self):
        """Cf. dict.clear"""
        dict.clear(self)
        dict.clear(self._flip)


if __name__=='__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS, verbose=True)
