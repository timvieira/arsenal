

def foo(x):
    y = yield 'foo: ' + x
    yield 'foo: ' + y


f = foo('hello')
print f.next()
print f.send('send')

