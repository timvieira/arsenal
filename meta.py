
import copy

def CopyInSubclass(*names):
    """
    Given a list of names of variables, this factory function return a metaclass which ensures
    that class variables corresponding to names will be copied when the class or subclasses are
    created (i.e., base classes will not reference the same instance).
    """
    class meta(type):
        def __init__(cls, name, bases, dict):
            for name in names:
                setattr(cls, name, copy.copy(getattr(cls, name)))
    return meta


if __name__ == '__main__':

    class A(object):
        __metaclass__ = CopyInSubclass('x','y')
        x = []
        y = 'original value'
    
    class B(A):
        pass

    class C(A):
        pass

    class D(B,C):
        pass
    
    a = A()
    b = B()
    c = C()
    d = D()

    print 'before:'
    print '  a.x:', a.x
    print '  b.x:', b.x
    print '  c.x:', c.x
    print '  d.x:', d.x
    
    a.x.append('A')
    b.x.append('B')
    c.x.append('C')
    d.x.append('D')
    
    print '\nafter:'
    print '  a.x:', a.x
    print '  b.x:', b.x
    print '  c.x:', c.x
    print '  d.x:', d.x
    
    print
    print 'a.y:', a.y
    print 'b.y:', b.y
    print 'c.y:', c.y
    print 'd.y:', d.y
    
    a.y = 'new value'
    B.y = 'B.y new value'
    b2 = B()
    
    assert B.y is b.y is b2.y
    assert A.y is not B.y is not A.y
    
    print 'a.y:', a.y
    print 'b.y:', b.y
    print 'c.y:', c.y
    
    import inheritance_diagram
