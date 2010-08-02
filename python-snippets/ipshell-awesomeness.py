"""
$ python greatest-snippet-ever.py 
foo:

In [1]: x = 100

In [2]: y.append(x)

In [3]: 
Do you really want to exit ([y]/n)? 
{'y': [100], 'x': 10}

"""

from IPython.Shell import IPShellEmbed

def foo():
    x = 10              # you are not going to be able to change me from IPShell
    y = []              # you can change me however
    IPShellEmbed([])()
    #import pdb; pdb.set_trace()
    return locals()

print 'foo:', foo()


