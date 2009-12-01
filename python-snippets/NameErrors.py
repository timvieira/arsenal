import sys

def ignorenames(f):

    def wrap(*args, **kwargs):
        successful = False
        # there might be more than one NameError in this function.
        # if we fail to hack the stack, we'll get stuck in an infinite loop
        # ALSO! since we might call this function many many times it must be idempotent
        # i.e., produce the same output and side-effect for every call with the same arguments
        while not successful:
            try:
                ret = f(*args, **kwargs)
            except NameError, exc_val:
                varname = str(exc_val)[len("global name '"):-len("' is not defined")]
                new_value = 'hacked_' + varname

                # hack the stack
                #frame = sys._getframe()
                #frame.f_globals[varname] = new_value
                #frame.f_locals[varname] = new_value

                # if you hack globals it sort of works...
                # BUT has the side-effect that it alters a global variable
                # we could just delete the names after we're done, but that would
                # effect thread-safety
                globals()[varname] = new_value

            else:
                successful = True
        return ret
    return wrap

try:
    del xyz
except NameError:
    pass

try:
    del abc
except NameError:
    pass

import lib.misc
lib.misc.assert_throws(NameError)(lambda : abc)()


def test():

    @ignorenames
    def test2():
        print '  test> xyz:', xyz
        print '  test> abc:', abc
    test2()

test()

print 'main> xyz:', xyz
print 'main> abc:', abc

lib.misc.assert_throws(NameError)(lambda : abc)()



