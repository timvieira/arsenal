
## I'm interested in creating a sanitation mechanism for 
## writing macros. With applications to improving the efficiency
## of function decorators

import inspect
import symtable

## I think you can do this all with inspect...


def get_symbols(fn):
    table = symtable.symtable(inspect.getsource(fn), 'string', 'exec')
    ns    = table.lookup(fn.__name__).get_namespace()
    ids   = ns.get_identifiers()
    return ids

def foo(x):
    y = x + 1
    return y

table = symtable.symtable("def foo(): pass", "string", "exec")

