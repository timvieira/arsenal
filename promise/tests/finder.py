
import promise

items = range(100)

def verify(finder):
    """Check that the given finder function works correctly."""
    assert finder(0)
    assert finder(42)
    assert not finder(101)
    assert not finder(1001)

def finder0(item):
    """Base 'finder' fuction; is quite stupid and slow."""
    i = 0
    while i < len(items):
        if items[i] == item:
            return True
        i += 1
    return False

@promise.invariant(["items"])
def finder1(item):
    """Finder function storing 'len' in a local variable."""
    i = 0
    while i < len(items):
        if items[i] == item:
            return True
        i += 1
    return False

@promise.sensible()
def finder2(item):
    """Finder function assumed to have sensible behaviour.

    'items' is considered invariant; 'len', 'True' and 'False' are constant.
    """
    i = 0
    while i < len(items):
        if items[i] == item:
            return True
        i += 1
    return False

