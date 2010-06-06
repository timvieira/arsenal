
import random
import promise

items = [random.randint(1,100) for _ in xrange(100)]

def aggregate0():
    i = 0
    total = 0
    while i < len(items):
        total += calculate(items[i])
        i += 1
    return total

@promise.pure()
def calculate(x):
    return 3*x*x - 2*x + (1 / x)

@promise.invariant(["items"])
def aggregate1():
    i = 0
    total = 0
    while i < len(items):
        total += calculate(items[i])
        i += 1
    return total

@promise.constant(["len"])
def aggregate2():
    i = 0
    total = 0
    while i < len(items):
        total += calculate(items[i])
        i += 1
    return total

@promise.constant(["calculate"])
def aggregate3():
    i = 0
    total = 0
    while i < len(items):
        total += calculate(items[i])
        i += 1
    return total

@promise.invariant(["items"])
@promise.constant(["len","calculate"])
def aggregate4a():
    i = 0
    total = 0
    while i < len(items):
        total += calculate(items[i])
        i += 1
    return total

@promise.sensible()
def aggregate4():
    i = 0
    total = 0
    while i < len(items):
        total += calculate(items[i])
        i += 1
    return total

def aggregate5():
    return sum([calculate(i) for i in items])

@promise.constant(["calculate"])
def aggregate6():
    return sum([calculate(i) for i in items])

