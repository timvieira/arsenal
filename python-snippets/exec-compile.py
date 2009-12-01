
def create_something(some_code, name):
    # Execute the template string in a temporary namespace and
    # support tracing utilities by setting a value for frame.f_globals['__name__']
    namespace = dict(__name__='temporary_namespace')

    exec some_code in namespace

    result = namespace[name]

    # from the python standard library collections module's implementation of namedtuple:
    #   For pickling to work, the __module__ variable needs to be set to the frame
    #   where the named tuple is created.  Bypass this step in enviroments where
    #   sys._getframe is not defined (Jython for example).
    import sys
    if hasattr(sys, '_getframe'):
        # we need to hack the stack b/c we're inside a function
        callerglobals = sys._getframe(1).f_globals
        result.__module__ = callerglobals.get('__name__', '__main__')

    return result

## WARNING:
##   I think that pickling might only work if the dynamically generated class is global
##   *AND* it must have the same name as in the code....
Foo = create_something(r"""
class Foo(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x \
                    and self.y == other.y \
                    and isinstance(self, other.__class__) \
                    and isinstance(other, self.__class__)
    def __repr__(self):
        return 'Foo({x},{y})'.format(x=self.x, y=self.y)
""", 'Foo')

def test_pickling():
    print 'test_pickling...'
    from pickle import dumps, loads
    p = Foo(1,2)
    assert p == loads(dumps(p))
    print 'pass.'

if __name__ == '__main__':
    test_pickling()


