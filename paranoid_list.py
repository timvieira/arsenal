
class SaferList(list):

    def notallowed(self, *args, **kw):
        raise AssertionError('Sorry, not allowed.')

    def __getitem__(self, item):
        assert self.boundscheck(item)
        return list.__getitem__(self, item)

    def boundscheck(self, item):
        return isinstance(item, int) and item >= 0 and item < list.__len__(self)

    def __getslice__(self, i, j):
        assert map(self.boundscheck, filter(None, (i,j))), 'getslice did not have idicies in bounds. %r' % ((i,j),)
        xx = list.__getslice__(self, i, j)
        assert len(xx) == (j-i), 'slices must have the proper size!'
        return SaferList(xx)

    append = notallowed
    pop = notallowed
    __setattr__ = notallowed
    __setitem__ = notallowed
    __setslice__ = notallowed
    __add__ = notallowed
    __contains__ = notallowed
    __delattr__ = notallowed
    __delitem__ = notallowed
    __delslice__ = notallowed
    __eq__ = notallowed
    __ge__ = notallowed
    __gt__ = notallowed
    __hash__ = notallowed
    __iadd__ = notallowed
    __imul__ = notallowed
    __le__ = notallowed
    __lt__ = notallowed
    __mul__ = notallowed
    __ne__ = notallowed
    __reduce__ = notallowed
    __reduce_ex__ = notallowed
    __reversed__ = notallowed
    __rmul__ = notallowed
    count = notallowed
    extend = notallowed
    index = notallowed
    insert = notallowed
    pop = notallowed
    remove = notallowed
    reverse = notallowed
    sort = notallowed

#    __getattribute__ = notallowed
#    __new__ = notallowed
#    __repr__ = notallowed
#    __subclasshook__ = notallowed
#    __class__ = notallowed
#    __doc__ = notallowed
#    __format__ = notallowed
#    __len__ = notallowed
#    __init__ = notallowed
#    __iter__ = notallowed
#    __sizeof__ = notallowed
#    __str__ = notallowed

