
# http://jtauber.com/blog/2008/11/28/thoughts_on_a_new_language/


"""
Python metaclasses. I only understood Python metaclasses after understanding the
following equivalence.

class <name> <bases>: 
    __metaclass__ = <metaclass> 
    <block>

is syntactic sugar for:
<name> = <metaclass>("<name>", <bases>, <dictionary created by executing block>)

You can think of the default metaclass for new-style classes is the builtin function 
type, but don't try accessing it, you'll get an AttributeError.

"""

def foo2(self):
    return 'bar'

def my_metaclass(name, bases, dic):
    print 'my_ metaclass invoked'
    return type(name, bases, dic)

class C(object):
    #__metaclass__ = type  # this is the default
    #__metaclass__ = my_metaclass

    x = 1
    #def foo(self):
    #    return 'bar'
    foo = foo2

C2 = type('C', (object,), {'x':1, 'foo':foo2})

for x in set(dir(C2) + dir(C)):
    a = getattr(C2, x)
    b = getattr(C, x)
    if a != b and x != '__dict__':
        print x


