import inspect

def callee():
    return inspect.getouterframes(inspect.currentframe())[1][3]

def caller():
    return inspect.getouterframes(inspect.currentframe())[2][3]


def anyfunction():
    print "Function %s \n called from %s" % (callee(), caller())


def test():
    def anotherfunction():
        anyfunction()
    anotherfunction()

test()
