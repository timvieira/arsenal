def complain(self, *wargs, **kwargs):
    if not hasattr(self, 'warning'):
        raise AssertionError
    if isinstance(self.warning, Exception):
        raise self.warning
    elif isinstance(self.warning, basestring):
        raise AssertionError(self.warning)
    else:
        raise AttributeError, self.warning


class ImmutableList(tuple):
    """
    A tuple-like object that raises useful errors when it is asked to mutate.

    Example::

        >>> a = ImmutableList(range(5))
        >>> a[3] = '4'
        Traceback (most recent call last):
            ...
        AssertionError
    """

    def __new__(cls, *args, **kwargs):
        return tuple.__new__(cls, *args, **kwargs)

    # All list mutation functions complain.
    __delitem__  = complain
    __delslice__ = complain
    __iadd__     = complain
    __imul__     = complain
    __setitem__  = complain
    __setslice__ = complain
    append       = complain
    extend       = complain
    insert       = complain
    pop          = complain
    remove       = complain
    sort         = complain
    reverse      = complain
    __setattr__  = complain
    __delattr__  = complain
    __mul__      = complain
    __rmul__     = complain


class InequalityComplaints(object):
    """ mixin which complains about greater and lessthan comparisons. """
    __ge__ = complain
    __gt__ = complain
    __le__ = complain
    __lt__ = complain


class SaferList(list, InequalityComplaints):
    """
    Immutable list which also ensures that slices have indicies strictly in bounds.
    """

    def __getitem__(self, item):
        assert self.boundscheck(item)
        return list.__getitem__(self, item)

    def boundscheck(self, item):
        return isinstance(item, int) and item >= 0 and item < list.__len__(self)

    def __getslice__(self, i, j):
        assert map(self.boundscheck, filter(None, (i,j))), 'getslice does not have indicies in bounds. %r' % ((i,j),)
        xx = list.__getslice__(self, i, j)
        assert len(xx) == (j-i), 'slices must have the proper size!'
        return SaferList(xx)

    append       = complain
    pop          = complain
    __setattr__  = complain
    __setitem__  = complain
    __setslice__ = complain
    __add__      = complain
    __contains__ = complain
    __delattr__  = complain
    __delitem__  = complain
    __delslice__ = complain
    __ge__       = complain
    __gt__       = complain
    __hash__     = complain
    __iadd__     = complain
    __imul__     = complain
    __le__       = complain
    __lt__       = complain
    __mul__      = complain
    __rmul__     = complain
    extend       = complain
    insert       = complain
    pop          = complain
    remove       = complain
    reverse      = complain
    sort         = complain

    # TODO: these methods might need special attention
    __eq__       = complain
    __ne__       = complain


# TODO: implement ImmutableDict
"""
class ImmutableDict(object):    
    @classmethod
    def fromkeys(cls, keys, value=None):
        instance = super(cls, cls).__new__(cls)
        instance.__init__(zip(keys, repeat(value)))
        return instance

    def __reduce_ex__(self, protocol):
        return type(self), (dict(self),)

    setdefault  = complain
    update      = complain
    pop         = complain
    popitem     = complain
    __setitem__ = complain
    __delitem__ = complain
    clear       = complain
""" 


if __name__ == '__main__':

    # TODO: add some tests
    def example():
        
        x = ImmutableList([])

    example()
