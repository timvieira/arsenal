import gc, sys

def find_names(obj):

    # step back as far as you can
    frame = sys._getframe()
    # weird, this is frame = frame.back until frame == None
    for frame in iter(lambda: frame.f_back, None):
        frame.f_locals

    result = set()
    for referrer in gc.get_referrers(obj):
        ## TODO:
        ##   we might want to get more information than the name
        ##   for example, which module, function, instance, or class
        ##   the reference is sitting in...
        if isinstance(referrer, dict):
            for k, v in referrer.iteritems():
                if v is obj:
                    result.add(k)
    return result

foo = []

def demo():
    bar = foo
    print find_names(bar)

#demo()
