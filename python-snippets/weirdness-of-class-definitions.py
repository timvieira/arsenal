

##class Foo:
##
##    print 'making class Foo.'
##
##    x = 10
##
##    for i in xrange(10):
##
##        def goo(self):
##            #print self.x
##            #print self.__class__.x
##            #print Foo.x
##
##            xxx = i
##            print xxx
##
##
##        class GOOF:
##            print 'trying to make GOOF class...'
##            #xxx = i
##            #print 'GOOF:', xxx
##            print i
##            print 'done making GOOD class'
##        
##        #print 'GOOF.xxx:', GOOF.xxx
##
##        print 'i:', i, goo
##
##    print 'end making class Foo'


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
