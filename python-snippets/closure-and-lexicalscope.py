# To see how lambda is broken, try generating a list of functions
# fs=[f0,...,f9] where fi(n)=i+n.

# First attempt:
fs = ((lambda n: i + n) for i in range(10))
#print 'fs[3](4) =', fs[3](4)

fs = list(fs)

print [f(4) for f in fs]

fs = []
for i in xrange(10):
    def f(n):
        return i+n
    fs.append(f)

# Still not working, so the reason is deeper, probably in the way
# environments are handled.

i = 1000
print
print 'setting i in lexical scope'
print [f(4) for f in fs]


print
#--
def xxx():
    fs = []
    for i in xrange(10):
        def f(n):
            return i+n
        fs.append(f)
    return fs
print 'Inside a function:'
print [f(4) for f in xxx()]
print '...at least lexical scope doesn\'t cause problems'


print
#--
def xxx():
    fs = []
    for i in xrange(10):
        def f(n):
            return i+n
        yield f
print 'with yield :', [f(4) for f in xxx()]
print 'yield-part2:', [f(4) for f in list(xxx())]


print
#--
print 'default parameter trick:'
fs = []
for i in xrange(10):
    def f(n, i=i):
        return i+n
    fs.append(f)
print [f(4) for f in fs]


print
#--
print 'function attribute trick:'
fs = []
for i in xrange(10):
    def f(n):
        return f.i+n
    f.i = i
    fs.append(f)
print [f(4) for f in fs]


print
#--
print 'closure on i after it exists a function:'
def make_f(i):
    def f(n):
        return i+n
    return f

fs = []
for i in xrange(10):
    fs.append(make_f(i))
print [f(4) for f in fs]

print 'theres stuff in f.func_closure:'
for f in fs:
    print f.func_closure[0].cell_contents,
print

print
#--
print 'class version (similar to function attribute):'
fs = []
for i in xrange(10):
    class f:
        i = i
        __call__ = lambda self, n: self.i + n
    f = f()
    fs.append(f)
print [f(4) for f in fs]


"""
print
#--
def closure(**env):  # DOESN'T WORK...
    def h(f):
        def g(*args, **kwargs):
            f.func_globals.update(env)
            return f(*args,**kwargs)
        return g
    return h

print 'closure dec + func_globals hack...'
def x100():
    fs = []
    for i in xrange(10):
        j = 0
        @closure(i=i,j=j)
        def f(n):
            assert j == 0
            return i+n
        fs.append(f)
    return fs
fs = x100()
j = 10
print [f(4) for f in fs]
"""



##print '--------------------------'
##
##def huh(env, name, value):
##    env[name] = value
##
##print 'this one works...'
##XXX = 'before'
##huh(locals(), 'XXX', 'after')
##print XXX == 'after'
##
##print 'this one doesnt...'
##def test():
##    XXX = 'before'
##    huh(locals(), 'XXX', 'after')
##    print XXX == 'after'
##test()

