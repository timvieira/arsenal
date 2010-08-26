## this on is really weird...
class A:
    a = 42

    # how is it that this works:
    b = a + 10

    c = (a + i for i in range(10))       # generator comprehension have function scope!

    # but this doesn't?
    try:
        c.next()
    except NameError:
        pass
    else:
        raise AssertionError

    # but whats so different from this one?
    d = [a + i for i in range(10)]

    # The Reason:
    #   The scope of names defined in a class block is limited to the 
    #   class block; it does not extend to the code blocks of methods 
    #   -- this includes generator expressions since they are implemented 
    #   using a *function scope*.


# A scope defines the visibility of a name within a block. 
# If a local variable is defined in a block, its scope includes 
# that block. If the definition occurs in a function block, the 
# scope extends to any blocks contained within the defining one, 
# unless a contained block introduces a different binding for the 
# name. 

"""
class Foo:
    print 'making class Foo.'
    x = 10
    for i in xrange(10):
        def goo(self):
            print self.x
            print self.__class__.x
            print Foo.x
            xxx = i
            print xxx
        class GOOF:
            print 'trying to make GOOF class...'
            xxx = i
            print 'GOOF:', xxx
            try:
                print i
            except NameError:
                pass
            print 'done making GOOD class'
        #print 'GOOF.xxx:', GOOF.xxx

        print 'i:', i, goo

    print 'end making class Foo'


try:
    del k
except NameError:
    pass

#class ROOF:
def ROOF():
    for k in xrange(5):

        class GOOF:
            print 'trying to make GOOF class...'
            print k
            my_k = k
            print 'done making GOOF class'
        
        print 'k:', k == GOOF().my_k == GOOF.my_k

    print 'ROOFUS?'
ROOF()

##f = Foo()
##
##try:
##    f.goo()
##except NameError:
##    pass
##else:
##    raise AssertionError('should have thrown a NameError')
##
##
##def goo2():
##
##    for i in xrange(10):
##
##        def goo():
##            xxx = i
##            print xxx
##
##        print 'i:', i, goo
##
##    return goo
##
##
##goo2()()

"""
