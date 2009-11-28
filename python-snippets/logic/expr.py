import re

class Expr(object):
    """
    Logical expression.

    In general, an Expr has an operator (op) and a list of arguments (args).

    Exprs can be constructed with operator overloading: if x and y are Exprs,
    then so are x + y and x & y, etc.  Also, if F and x are Exprs, then so is 
    F(x).

    See http://www.python.org/doc/current/ref/specialnames.html to learn more
        about operator overloading in Python.

    WARNING: x == y and x != y are NOT Exprs.  The reason is that we want
    to write code that tests 'if x == y:' and if x == y were the same
    as Expr('==', x, y), then the result would always be true; not what a
    programmer would expect.
    
    WARNING: if x is an Expr, then so is x + 1, because the int 1 gets
    coerced to an Expr by the constructor.  But 1 + x is an error, because
    1 doesn't know how to add an Expr.  (Adding an __radd__ method to Expr
    wouldn't help, because int.__add__ is still called first.) Therefore,
    you should use Expr(1) + x instead, or ONE + x, or expr('1 + x').
    """

    def __init__(self, op, *args):
        """ op is a string; args are Exprs (or are coerced to Exprs). """
        self.op = op
        self.args = map(expr, args)   ## Coerce args to Exprs

    def sexp(self):
        if not self.args:
            return '(%s)' % (self.op,)
        return '(%s %s)' % (self.op, ' '.join(map(Expr.sexp, self.args)))

    def __call__(self, *args):
        """Self must be a symbol with no args, such as Expr('F').  Create a new
        Expr with 'F' as op and the args as arguments. """
        assert is_symbol(self.op) and not self.args         # no F(x)(y) or a.F(x)
        return Expr(self.op, *args)

    def __repr__(self):
        """ Show something like 'P' or 'P(x, y)', or '~P' or '(P | Q | R)' """
        # Constant or proposition with arity 0
        if len(self.args) == 0:
            return str(self.op)
        # Functional or Propositional operator
        elif is_symbol(self.op):
            return '%s(%s)' % (self.op, ', '.join(map(repr, self.args)))
        # Prefix operator
        elif len(self.args) == 1:
            return self.op + repr(self.args[0])
        # Infix operator
        else:
            # this just makes it look nicer
            if self.op == '.':
                return '(%s)' % '.'.join(map(repr, self.args))
            else:
                return '(%s)' % (' '+self.op+' ').join(map(repr, self.args))

    def __eq__(self, other):
        """ x and y are equal iff their ops and args are equal. """
        return (other is self) or (isinstance(other, Expr)
            and self.op == other.op and self.args == other.args)

    def __hash__(self):
        """ Need a hash method so Exprs can live in dicts."""
        return hash(self.op) ^ hash(tuple(self.args))

    def __and__(self, other):     return Expr('And',  self, other)
    def __invert__(self):         return Expr('Not',  self)
    def __lshift__(self, other):  return Expr('Implies', other, self)
    def __rshift__(self, other):  return Expr('Implies', self, other)
    def __or__(self, other):      return Expr('Or',  self, other)
    def __getattr__(self, attr):  return Expr('.', self, attr)


def Not(x):
    return not x

def And(x,y):
    return x and y

def Or(x,y):
    return x or y

def Implies(p,q):
    return not p or q

def is_symbol(s):
    """ a symbol is a string that starts with an alphabetic char. """
    return isinstance(s, str) and (s[0].isalpha() or s[0] == '?')

def is_var_symbol(x):
    """ a lowercase symbol is a variable. """
    if isinstance(x, Expr):
        return is_var_symbol(x.op) and len(x.args) == 0
    return is_symbol(x) and x.islower()



def expr(s):
    """Create an Expr representing a logic expression by parsing the input
    string. Symbols and numbers are automatically converted to Exprs.

    But BE CAREFUL; precedence of implication is wrong. expr('P & Q ==> R & S')
    is ((P & (Q >> R)) & S); so you must use expr('(P & Q) ==> (R & S)').
    """
    if isinstance(s, Expr):
        return s
    ## Replace a symbol or number, such as 'P' with 'Expr("P")'
    try:
        s = re.sub(r'([a-zA-Z0-9_.]+)', r'Expr("\1")', s)
    except TypeError:
        return s
    ## Now eval the string.  (A security hole; do not use with an adversary.)
    return eval(s, {'Expr':Expr})


def subst(s, x):
    """Substitute the substitution s into the expression x.
    >>> subst({x: 42, y:0}, F(x) + y)
    (F(42) + 0)
    """
    if isinstance(x, list): 
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple): 
        return tuple([subst(s, xi) for xi in x])
    elif not isinstance(x, Expr): 
        return x
    elif is_var_symbol(x.op): 
        return s.get(x, x)
    else: 
        return Expr(x.op, *[subst(s, arg) for arg in x.args])



def ForAll(var, expression):

    def partially_eval(var, expression):
        return eval(repr([subst({var:val}, expression) for val in var.domain]))

    if isinstance(expression, list):
        partialeval = []
        for e in expression:
            partialeval.extend(partially_eval(var, e))

    elif isinstance(expression, Expr):
        partialeval = partially_eval(var, expression)

    elif isinstance(expression, float):
        return expression   # looks like the expression has already been evaluated...

    else:
        raise AssertionError('busted...')

    if all(isinstance(x,bool) for x in partialeval):
        return partialeval.count(True) * 1.0 / len(partialeval)
    else:
        return partialeval          # should create an expression instead of a list...


def isground(expr):
    if not isinstance(expr, Expr):
        return True
    if is_var_symbol(expr):
        return False
    return all(isground(arg) for arg in expr.args)

def relation(fn):
    def wrap(*args):
        if all(isground(arg) for arg in args):
            return fn(*args)
        else:
            return Expr(fn.__name__, *args)
    return wrap

def Var(name, domain_or_type):
    e = expr(name)
    try:
        e.domain = domain_or_type.domain
    except AttributeError:
        e.domain = domain_or_type
    return e




## Right now these objects need to be in the global namespace

class Person(object):
    domain = set()
    def __init__(self, name):
        self.name   = name          # name must be the same as the atom used
        self.spouse = None
        self.smokes = False
        Person.domain.add(self)
    def __repr__(self):
        return self.name

@relation
def Friends(a,b):
    return a.spouse == b


Bob = Person('Bob')
Anna = Person('Anna')
Bob.smokes = True
Anna.smokes = True
Bob.spouse = Anna
Anna.spouse = Bob

Ricky = Person('Ricky')
Lucy = Person('Lucy')
Ricky.smokes = True
Lucy.smokes = False
Ricky.spouse = Lucy
Lucy.spouse = Ricky

x = Var('x', Person)
y = Var('y', Person)
z = Var('z', Person)

Rule1 = (x.spouse.smokes & Friends(x, x.spouse)) >> x.smokes
Rule2 = (x.smokes & Friends(x, y)) >> y.smokes
Rule3 = (Friends(x, y) & Friends(y, z)) >> Friends(x, z)


print
print '1:', Rule1
print ForAll(x, Rule1)
print
print '2:', Rule2
print ForAll(x, Rule2)
print ForAll(y, ForAll(x, Rule2))
print
print '3:', Rule3
print ForAll(z, ForAll(y, ForAll(x, Rule3)))


