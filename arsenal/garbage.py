import gc
from functools import wraps

def dump_garbage():
    """
    Show us what's in the garbage!

    Make a leak:
      >>> l = []
      >>> l.append(l)
      >>> del l

    Show the dirt:
      >>> dump_garbage()
      GARBAGE:
        list: [[...]]

    """
    gc.enable()
    gc.set_debug(gc.DEBUG_LEAK)

    # force collection
    gc.collect()

    print "GARBAGE:"
    for x in gc.garbage:
        s = repr(x)
        if len(s) > 80:   # TODO: create a humanreadable for snippet repr size.
            s = s[:30] + ' ... ' + s[-30:]
        print '  %s: %s' % (type(x).__name__, s)


def garbagecollect(f):
    """ Decorate a function to invoke the garbage collecter after each execution. """
    @wraps(f)
    def inner(*args, **kwargs):
        result = f(*args, **kwargs)
        gc.collect()
        return result
    return inner

