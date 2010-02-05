from time import time

class A(object):
#    __slots__ = ('a',)
    def __init__(self):
        for i in xrange(1000):
            setattr(self, 'a%s'%i, i)

class B(object):
#    __slots__ = ('A',)
    def __init__(self):
        for i in xrange(1000):
            setattr(self, 'A%s'%i, i)


def run(a):
    N = 100000
    start = time()
    for i in range(N):
        try:
            a.a1
        except:
            pass
    t1 = time() - start
    
    start = time()
    for i in range(N):
        if hasattr(a,'a'):
            a.a1
    t2 = time() - start
    
    start = time()
    for i in range(N):
        if isinstance(a, A):
            a.a1
    t3 = time() - start

    #getattr(a, 'a1', None) or a.A1
    
    print 'try catch: ', t1
    print 'hasattr:   ', t2
    print 'isinstance:', t3
    print

run(A())     
run(B())
