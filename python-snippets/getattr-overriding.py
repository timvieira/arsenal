
##
# Overriding the behavior of getattr and setattr is a bit quirky.
#
# object.__getattr__(self, attr) will only be called if python does not find the
#   attribute name attr in "the usual place" (i.e., "attr not in self.__dict__").
#
# Thus, you must to put attrs which you want to override in "an unusual place", which
#    requires you do override __setattr__ as well.
#
# Note: regardless of whether of not you override __getattr__ you can always call
#   __getattribute__ to get the standard behavior.
##
class foo(object):
    def __init__(self):
        # __dict__ is in "the usual place" lets use this to create "an unusual place"
        # where we will store things indirectly
        self.__dict__['_unusual_place'] = {}

    def __getattr__(self, attr):
        return 'GETATTR(%s)' % self._unusual_place.get(attr, None)

    def __setattr__(self, attr, val):
        self._unusual_place[attr] = 'SETATTR(%s)' % val


if __name__ == '__main__':
    x = foo()

    print x.foo
    x.foo = 'gooooood'
    print x.foo
    print getattr(x, 'foo')

    # this should NOT work
    #print x.__getattribute__('foo')

    # this should work
    print x.__getattribute__('__dict__')

    print x.__dict__
