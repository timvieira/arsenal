"""

  promise:  bytecode optimisation using staticness assertions.

This is a module for applying some simple optimisations to function bytecode.
By promising that a function doesn't do certain things at run-time, it's
possible to apply optimisations that are not legal in the general case.

As a simple example, it's possible to promise that a function doesn't modify
(or care if anyone else modifies) any builtin functions by decorating it thus:

    @promise.constant(__builtins__)
    def function():
        ...

Such a promise will allow the builtins to be stored as direct object references
in the function bytecode, avoiding name lookups during function execution.

As another example, it's possible to promise that a function is pure; i.e. that
it's a simple algorithm for mapping input values to an output value:

    @promise.pure()
    def calculate(a,b):
        return 2*a*a + 3*b + 7

If a pure function is then used by another function as a constant, it can be
directly inlined into the bytecode to avoid the overhead of a function call:

    @promise.constant(("calculate",))
    def aggregate(pairs):
        #  calculate() is a pure constant, so it will be inlined here.
        return sum(calculate(a,b) for (a,b) in pairs)

The currently available promises are:

    * invariant(names):  promise that variables having the given names will
                         not change value during execution of the function.

    * constant(names):   promise that variables having the given names will
                         always refer to the same object, across all calls
                         to the function.

    * pure():   promise that the function is a transparent mapping from inputs
                to outputs; this opens up the possibility of inling it directly
                into other functions.

    * sensible():   promise that the function is "sensibly behaved".  All
                    builtins and module-level functions are considered
                    constant; all other module-level names are considered
                    invariant.

Promise is built on Noam Raphael's fantastic "byteplay" module; since the
official byteplay distribution doesn't support Python 2.6, a local version with
appropriate patches is included with promise.
"""


__ver_major__ = 0
__ver_minor__ = 2
__ver_patch__ = 1
__ver_sub__ = ""
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,
                              __ver_patch__,__ver_sub__)


import types

from promise.byteplay import *


class BrokenPromiseError(Exception):
    """Exception raised when you make a promise that is provably broken."""
    pass


def _ids():
    """Generator producing unique ids."""
    i = 0
    while True:
        i += 1
        yield i 
_ids = _ids()


def new_name(name=None):
    """Generate a new unique variable name

    If the given name is not None, it is included in the generated name for
    ease of reference in e.g. tracebacks or bytecode inspection.
    """
    if name is None:
        return "_promise_var%s" % (_ids.next(),)
    else:
        return "_promise_var%s_%s" % (_ids.next(),name,)


def apply_deferred_promises(func):
    """Apply any deferred promises attached to a function."""
    #  Get the code object before checking for deferred promises.
    #  This prevents race conditions if several threads apply them at once.
    c = Code.from_code(func.func_code)
    try:
        deferred = func._promise_deferred
    except AttributeError:
        pass
    else:
        del func._promise_deferred
        #  Remove the bootstrapping code inserted by Promise.defer()
        idx = c.code.index((POP_TOP,None))
        del c.code[:idx+1]
        #  Apply each promise in turn
        for p in deferred:
            p.apply(func,c)
        #  Use the transformed bytecode in subsequent calls to func
        func.func_code = c.to_code()
    pass


class Promise(object):
    """Base class for promises.

    A "Promise" represents a transformation that can be applied to a function's
    bytecode, given that the user promises to only use the function in certain
    restricted ways.  They are intended for use as function- or class-level
    decorators.  The following methods should be provided by subclasses:

        * decorate(func):  mark the given function as having this promise
                           applied; this may directly modify the function's
                           bytecode or defer the modification until call time.

        * apply(func,code):  actually transform the function's bytecode
                             to take advantages of the promised behaviour.

    Subclasses may find the following method useful:

        * defer(func):  defer the application of this promise until the
                        given function is called for the first time. 

        * apply_or_defer(func):  immediately apply this promise if the given
                                 function has no deferred promises; otherwise
                                 defer it until after the existing promises.
    """

    def __init__(self):
        pass

    def __call__(self,*args):
        """Apply this promise to a function, module, dict, etc.

        Calling a promise arranges for it to be applied to any functions
        found in the given arguments.  Each argument can be a raw function,
        or a class, module or iterable of functions.
        """
        if not args:
            return None
        for arg in args:
            if isinstance(arg,types.FunctionType):
                self.decorate(arg)
            else:
                try:
                    subargs = arg.itervalues()
                except (AttributeError,TypeError):
                    subargs =  (getattr(arg,nm) for nm in dir(arg))
                for subarg in subargs:
                    if isinstance(subarg,types.FunctionType):
                        self(subarg)
        return args[0]

    def decorate(self,func):
        """Decorate the given function to apply this promise.

        This can either directly apply the promise, or defer its application
        until the function is first executed.  The return value is ignored;
        in practice this means that decorate() must directly modify the given
        function rather than the standard practice of creating a wrapper.
        """
        pass

    def apply(self,func,code):
        """Apply this promise to the given function.

        The argument 'func' is the function to which the promise is being
        applied, and 'code' is a byteplay code object representing its code.
        The code object should be modified in-place.
        """
        pass

    def defer(self,func):
        """Defer the application of this promise func is first executed."""
        # Try to be thread-safe by using setdefault(), which is implemented
        # in C and is therefore non-interruptible.
        default = []
        deferred = func.__dict__.setdefault("_promise_deferred",default)
        deferred.append(self)
        if deferred is default:
            #  Add code to apply the promise when func is first executed.
            #  These opcodes are removed by apply_deferred_promises()
            c = Code.from_code(func.func_code)
            c.code.insert(0,(LOAD_CONST,apply_deferred_promises))
            c.code.insert(1,(LOAD_CONST,func))
            c.code.insert(2,(CALL_FUNCTION,1))
            c.code.insert(3,(POP_TOP,None))
            func.func_code = c.to_code()

    def apply_or_defer(self,func):
        """Apply this promise, or defer it if others are already deferred.

        It's generally a good idea to use this instead of directly applying
        a promise, since it ensures that individual promises will be applied
        in the order in which they appear in code.
        """
        try:
            deferred = func._promise_deferred
        except AttributeError:
            code = Code.from_code(func.func_code)
            self.apply(func,code)
            func.func_code = code.to_code()
        else:
            deferred.append(self)


class invariant(Promise):
    """Promise that the given names are invariant during the function call.

    This promise allows the names to be loaded once, at the beginning of the
    function, and accessed through local variables from there on out.  Instead
    of doing this:

        myvar = SomeGlobalObject()
        def myfunc():
            l_myvar = myvar  # store locally for faster access
            ...do stuff with l_myvar...

    You can now do this:

        myvar = SomeGlobalObject()
        @promise.invariant(("myvar",))
        def myfunc():
            ...do stuff directly with myvar...

    """

    def __init__(self,names):
        self.names = names
        super(invariant,self).__init__()

    def decorate(self,func):
        self.apply_or_defer(func)

    def apply(self,func,code):
        local_names = {}
        load_ops = []
        for (i,(op,arg)) in enumerate(code.code):
            #  Replace any LOADs of invariant names with a LOAD_FAST
            if op in (LOAD_GLOBAL,LOAD_NAME,LOAD_DEREF):
                if arg in self.names:
                    if arg not in local_names:
                        local_names[arg] = new_name(arg)
                        load_ops.append((op,arg))
                        load_ops.append((STORE_FAST,local_names[arg]))
                    code.code[i] = (LOAD_FAST,local_names[arg])
            #  Quick check that invariant names arent munged
            elif op in (STORE_NAME,STORE_GLOBAL,STORE_FAST,STORE_DEREF):
                if arg in self.names:
                    msg = "name '%s' was promised invariant, but assigned to"
                    raise BrokenPromiseError(msg % (arg,))
            elif op in (DELETE_NAME,DELETE_GLOBAL,DELETE_FAST):
                if arg in self.names:
                    msg = "name '%s' was promised invariant, but deleted"
                    raise BrokenPromiseError(msg % (arg,))
        #  Insert code to load the names in local vars at start of function
        for i,op in enumerate(load_ops):
            code.code.insert(i,op)


class constant(Promise):
    """Promise that the given names are constant

    This promise allows the objects referred to by the names to be stored
    directly in the code as constants, eliminating name lookups.  We try
    to resolve all constants at decoration time, but any that are missing
    will be deferred until the function first executes.

    Instead of doing this:

        # this trick makes range() a local constant
        def yield_lots_of_ranges(range=range):
            for i in range(10):
                yield range(i)

    You can now do this:

        @promise.constant(("range",))
        def yield_lots_of_ranges()
            for i in range(10):
                yield range(i)

    """

    def __init__(self,names,exclude=[]):
        self.names = names
        self.exclude = exclude
        super(constant,self).__init__()

    def _load_name(self,func,name,op=None):
        """Look up the given name in the scope of the given function.

        This is an attempt to replicate the name lookup rules of LOAD_NAME,
        LOAD_GLOBAL and friends.  If a specific bytecode op is specified,
        only the rules for that operation are applied.

        If the name cannot be found, NameError is raised.
        """
        if op in (None,LOAD_NAME,LOAD_DEREF):
           try:
               return self._load_name_deref(func,name)
           except NameError:
               pass
        if op in (None,LOAD_NAME,LOAD_GLOBAL):
           try:
               return self._load_name_global(func,name)
           except NameError:
               pass
        raise NameError(name)
 

    def _load_name_deref(self,func,name):
        """Simulate (LOAD_DEREF,name) on the given function."""
        #  Determine index of cell matching given name
        try:
            idx = func.func_code.co_cellvars.index(name)
        except ValueError:
            try:
                idx = func.func_code.co_freevars.index(name)
                idx -= len(func.func_code.co_cellvars)
            except ValueError:
                raise NameError(name)
        return func.func_closure[idx].cell_contents

    def _load_name_global(self,func,name):
        """Simulate (LOAD_GLOBAL,name) on the given function."""
        try:
            try:
                return func.func_globals[name]
            except KeyError:
                return __builtins__[name]
        except KeyError:
            raise NameError(name)

    def decorate(self,func):
        try:
            self.apply_or_defer(func)
        except NameError:
            self.defer(func)

    def apply(self,func,code):
        new_constants = {}
        old_constants = set()
        missing_names = []
        for (i,(op,arg)) in enumerate(code.code):
            #  Replace LOADs of matching names with LOAD_CONST
            if op in (LOAD_GLOBAL,LOAD_DEREF,LOAD_NAME):
                if arg in self.names:
                    if arg in self.exclude or arg in missing_names:
                        continue
                    try:
                        val = new_constants[arg]
                    except KeyError:
                        try:
                            val = self._load_name(func,arg,op)
                        except NameError:
                            missing_names.append(arg)
                        else:
                            new_constants[arg] = val
                            code.code[i] = (LOAD_CONST,val)
                    else:
                        code.code[i] = (LOAD_CONST,val)
            #  Quick check that locals haven't been promised constant
            elif op == LOAD_FAST:
                if arg in self.names:
                    raise BrokenPromiseError("local names can't be constant: '%s'" % (arg,))
            #  Quick check that constant names arent munged
            elif op in (STORE_NAME,STORE_GLOBAL,STORE_FAST,STORE_DEREF):
                if arg in self.names:
                    msg = "name '%s' was promised constant, but assigned to"
                    raise BrokenPromiseError(msg % (arg,))
            elif op in (DELETE_NAME,DELETE_GLOBAL,DELETE_FAST):
                if arg in self.names:
                    msg = "name '%s' was promised constant, but deleted"
                    raise BrokenPromiseError(msg % (arg,))
            #  Track any existing constants for use in the next step
            elif op == LOAD_CONST:
                if arg not in old_constants:
                    old_constants.add(arg)
                #  Recursively apply promise to any inner functions.
                #  TODO: how can we do deferred promises on inner functions?
                if i+1 < len(code.code):
                    (nextop,nextarg) = code.code[i+1]
                    if nextop in (MAKE_FUNCTION,MAKE_CLOSURE):
                        exclude = arg.to_code().co_varnames
                        p = self.__class__(names=self.names,exclude=exclude)
                        try:
                            p.apply(func,arg)
                        except NameError:
                            pass
        #  If any constants define a '_promise_fold_constant' method,
        #  let them have a crack at the bytecode as well.
        for const in new_constants.itervalues():
            try:
                fold = const._promise_fold_constant
            except AttributeError:
                pass
            else:
                fold(func,code)
        for const in old_constants:
            try:
                fold = const._promise_fold_constant
            except AttributeError:
                pass
            else:
                fold(func,code)
        #  Re-raise a NameError if any occurred
        if missing_names:
            raise NameError(",".join(missing_names))


class pure(Promise):
    """Promise that a function is pure.

    A pure function has no side-effects or internal state; it is simply
    a mapping from input values to output values.

    Currently the only optimisation this enables is inlining of constant
    pure functions; other optimisations may be added in the future.  For
    example, in this code the calculate() function will be inlined as if
    it were a macro:

        @promise.pure()
        def calculate(a,b):
            reutrn a*a + 3*b + 7

        @promise.constant(("calculate",))
        def aggregate(pairs):
            return sum(calculate(a,b) for (a,b) in pairs)

    """

    def decorate(self,func):
        c = Code.from_code(func.func_code)
        if c.varargs:
            raise TypeError("pure functions currently don't support varargs")
        if c.varkwargs:
            raise TypeError("pure functions currently don't support varkwds")
        func._promise_fold_constant = self._make_fold_method(func)
        #  Since I'm pure, my globals must all be constant
        global_names = set()
        for (op,arg) in Code.from_code(func.func_code).code:
            if op == LOAD_GLOBAL:
                global_names.add(arg)
            elif op in (STORE_GLOBAL,DELETE_GLOBAL):
                msg = "pure functions must not modify their globals: '%s'"
                raise BrokenPromiseError(msg % (arg,))
        constant(global_names).decorate(func)

    def _make_fold_method(self,source_func):
        """Make _promise_fold_constant method for the given pure function."""
        def fold(dest_func,dest_code):
            """Inline the code of source_func into the given bytecode."""
            #  Apply any deferred promises to source_func.
            #  Since it's pure, we can simply call it to force this.
            if hasattr(source_func,"_promise_deferred"):
                try:
                    source_func(*([None]*source_func.func_code.co_argcount))
                except Exception:
                    pass
            #  Inline the function at every callsite
            toinline = self._find_inlinable_call(source_func,dest_code)
            while toinline is not None:
                (loadsite,callsite) = toinline
                #  Give new names to the locals in the source bytecode
                source_code = Code.from_code(source_func.func_code)
                name_map = self._rename_local_vars(source_code)
                #  Remove any setlineno ops from the source bytecode
                new_code = [c for c in source_code.code if c[0] != SetLineno]
                source_code.code[:] = new_code
                #  Pop the function arguments directly from the stack.
                #  Keyword args are currently not supported.
                numargs = dest_code.code[callsite][1] & 0xFF
                for i in xrange(numargs):
                    argname = source_func.func_code.co_varnames[i]
                    source_code.code.insert(0,(STORE_FAST,name_map[argname]))
                #  Fill in any missing args from the function defaults
                numreqd = source_func.func_code.co_argcount
                for i in xrange(numargs,numreqd):
                    argname = source_func.func_code.co_varnames[i]
                    defidx = i - numreqd + len(source_func.func_defaults)
                    defval = source_func.func_defaults[defidx]
                    source_code.code.insert(0,(STORE_FAST,name_map[argname]))
                    source_code.code.insert(0,(LOAD_CONST,defval))
                #  Munge the source bytecode to leave return value on stack
                end = Label()
                source_code.code.append((end,None))
                for (i,(op,arg)) in enumerate(source_code.code):
                    if op == RETURN_VALUE:
                        source_code.code[i] = (JUMP_ABSOLUTE,end)
                #  Replace the callsite with the inlined code
                dest_code.code[callsite:callsite+1] = source_code.code
                del dest_code.code[loadsite]
                #  Rinse and repeat
                toinline = self._find_inlinable_call(source_func,dest_code)
        return fold

    def _find_inlinable_call(self,func,code):
        """Find an inlinable call to func in the given code.

        If such a call is found, a tuple (loadsite,callsite) is returned
        giving the position of the LOAD_CONST on the function and the matching
        CALL_FUNCTION.  If no inlinable call is found, returns None.
        """
        for (i,(op,arg)) in enumerate(code.code):
            if op == LOAD_CONST and arg == func:
                loadsite = i
                callsite = self._find_callsite(loadsite,code.code)
                if callsite is not None:
                    (op,arg) = code.code[callsite]
                    #  Can't currently inline kwdargs
                    if arg == (arg & 0xFF):
                        return (loadsite,callsite)
        return None

    def _find_callsite(self,idx,code):
        """Find index of the opcode calling the value pushed at opcode idx.

        This method finds the position of the opcode that calls a function
        pushed onto the stack by opcode 'idx'.  If we cannot reliably find
        such an opcode (due to weird branching etc) then None is returned.
        """
        try:
            callsite = idx + 1
            try:
                (curop,curarg) = code[callsite]
            except IndexError:
                return None
            (pop,push) = getse(curop,curarg)
            curstack = push - pop
            while curstack > 0 or curop != CALL_FUNCTION:
                callsite += 1
                try:
                    (curop,curarg) = code[callsite]
                except IndexError:
                    return None
                (pop,push) = getse(curop,curarg)
                curstack = curstack + push - pop
            if curstack == 0:
                return callsite
            else:
                return None
        except ValueError:
            return None

    def _rename_local_vars(self,code):
        """Rename the local variables in the given code to new unique names.

        Returns a dictionary mapping old names to new names.
        """
        name_map = {}
        for nm in code.to_code().co_varnames:
            name_map[nm] = new_name(nm)
        for (i,(op,arg)) in enumerate(code.code):
            if op in (LOAD_FAST,STORE_FAST,DELETE_FAST):
                try:
                    newarg = name_map[arg]
                except KeyError:
                    newarg = new_name(arg)
                    name_map[arg] = newarg
                code.code[i] = (op,newarg)
        return name_map


class sensible(Promise):
    """Promise that a function is sensibly behaved.  Basically:

        * all builtins are constant
        * all global functions are constant
        * all other globals are invariant

    The semantics of this promise will probably change as more types of promise
    are added to the module.
    """

    def decorate(self,func):
        self.defer(func)

    def apply(self,func,code):
        callable_globals = set()
        other_globals = set()
        for (nm,obj) in func.func_globals.iteritems():
            if callable(obj):
                callable_globals.add(nm)
            else:
                other_globals.add(nm)
        constant(__builtins__).apply(func,code)
        constant(callable_globals).apply(func,code)
        invariant(other_globals).apply(func,code)
 

