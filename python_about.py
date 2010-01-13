#
# pyconfig.py:
#
# This module essentially performs introspection on the
# Python interpreter itself, to discover which language
# features are available.
#
# At first glance, this seems crazy -- why not just check
# sys.version_info? Well, for example:
#
#	o You could be running under a nonstandard/alternative
#	  Python implementation (e.g. Jython, or maybe a cut-down
#	  embedded version that eliminated some features) and you
#	  want to dynamically figure out what is available.
#
#	o It seems more self-documenting to write something like:
#
#		  if Have_Iterators():
#				 ... do something with iterators ...
#
#		Than to write:
#
#		  if sys.version_info[0] >= 2 and sys.version_info[1] >= 2:
#				 ... do something with iterators ...
#
#	  In other words, your code now says "here is the capability
#	  I need", making it more maintainable down the road than
#	  a hardcoded version match. Plus, it is more robust in
#	  the presence of a nonstandard interpreter.
#
#	o You're writing an installer, and want to pick different
#	  modules to install, based on platform.
#
#	o Some oddball (or future) version of Python might break
#	  sys.version_info (expand the number of values, etc.), so you
#	  don't want to rely on it.
#

# This code may be freely used, modified and distributed, but I'd
# appreciate a copy of any fixes/enhancements.
#
#	 -- Frank McIngvale (frankm@hiwaay.net)

# (Possible) TODO: Enhance tests to verify correctness of results, not
#				   just that each testcase compiles & runs OK.

# Note: Compatibility with Python 1.5 is required here.
import __builtin__, string

# FYI, there are tests for these PEPs:
#
# PEP 227 - nested scopes
# PEP 232 - function attributes
# PEP 236 - __future__ directive
# PEP 207 - rich comparisons
# PEP 279 - enumerate
# PEP 218 - builtin sets
# PEP 234 - iterators
# PEP 255 - generators
# PEP 237 - promoting ints to longs
# PEP 238 - true division
# PEP 289 - generator expressions
# PEP 252/253 - newstyle classes (check existance via Have_Object())
# PEP 318 - decorators
# PEP 322 - reverse iteration
# PEP 328 - multiline imports
# PEP 292 - $ string substitution
# PEP N/A - augmented assignment ('+=')
# PEP N/A - list comprehensions
# PEP N/A - import NAME as OTHERNAME
# PEP N/A - string methods
# PEP N/A - unicode
# PEP N/A - basestring class
# PEP N/A - longs > sys.maxint in range()
# PEP N/A - call dict() with keywords
# PEP N/A - 'bool' as a class
#
# Notable PEP's not tested:
# PEP 205 - weak refs (use Have_Module("weakref") instead)
# PEP 208 - new coercion model
#			(can you test this at the Python level?)
# PEP 217 - interactive display hook
# PEP 229 - build system [involves building Python itself]
# PEP 230 - warning framework [don't see a need to test for this]
# PEP 235 - case sensitivity in import
#			[would rather not create tempfiles in order to test this]
# PEP 237 - Warnings on int->long promotion [don't see a need to test]
# PEP 241 - metadata in packages
#			[this is a convention for packages, has nothing to do w/language]
# PEP 324 - subprocess -- use Have_Module("subprocess")
# PEP 327 - Decimal type -- use Have_Module("decimal")
# PEP 331 - locale independent float/string conversion
#			[does this only affect C extensions?]
#

# when developing new tests, it's a good idea to turn this
# on to make sure the correct exceptions are being raised.
SHOW_DEBUG_INFO = 0

def compile_code( codestr ):
    # compiler module is not available under older Pythons,
    # so I adapted the following from py_compile.py
    codestr = string.replace(codestr, "\r\n","\n")
    codestr = string.replace(codestr,"\r","\n")	
    if codestr and codestr[-1] != '\n':
        codestr = codestr + '\n'

    return __builtin__.compile(codestr, 'dummyname', 'exec')

def can_run_code( codestr ):
    try:
        eval( compile_code(codestr) )
        return 1
    except Exception,exc:
        if SHOW_DEBUG_INFO:
            print "RUN EXC ",str(exc)
            
        return 0

def Have_Module( module_name ):
    "Check for the existance of the named module."
    return can_run_code("import %s\ndel %s\n" % (module_name,module_name))

def Have_TrueFalse():
    "Does this Python support True/False builtins?"
    return can_run_code('a = __builtin__.True')

def Have_ObjectClass():
    """
    Does this Python have builtin 'object' class?
    (This also means that you have newstyle classes, as
    well as builtin classes 'dict', 'list', 'int', etc.)
    """
    return can_run_code('class foo(object):\n\tpass')

slots_testcode = """
class foo(object):
    __slots__ = ('aaa','bbb')

f = foo()
try:
    f.ccc = 1
    raise "BAD SLOTS"
except AttributeError:
    pass
"""

def Have_Slots():
    """Does this Python recognize object __slots__?"""
    return can_run_code(slots_testcode)

def Have_BoolClass():
    """
    Does this Python have 'bool' as a class (instead of a function)?
    """
    # A little different than above: Since bool can't be a
    # base class, and there is also a bool function in 2.2,
    # you have to be careful to not grab the wrong thing.
    return can_run_code('issubclass(bool, object)')

def IsLegal_BaseClass( classname ):
    "Is it legal to subclass the given classname?"
    return can_run_code('class f(%s): pass' % classname)

# formatting is a little easier if the code fragments are
# sitting outside the functions that use them
iter_test_code = """
class iter_test:
    def __iter__(self): return self
    def next(self): raise StopIteration

for n in iter_test():
    pass
"""

def Have_Iterators():
    "Does this Python support iterators?"
    return can_run_code(iter_test_code)

def Have_Future():
    "Does this Python support 'from __future__ ...'?"
    return can_run_code('import __future__')

generator_test_code = """
def test_generate(N): yield N
test_generate(4)
"""

def Have_Generators():
    "Does this Python have generators?"
    
    s = ''	
    # older Pythons don't have __future__, and the way __future__
    # works, you can't put it inside a try..except, so I have to
    # modify the code dynamically.
    if Have_Future(): 
        # need this for Python 2.2 to support generators
        s = s + "from __future__ import generators\n"

    s = s + generator_test_code
    
    return can_run_code(s)

def Have_TrueDivision():
    "Does this Python support true division (i.e. 1/2 == 0.5)?"
    
    s = ''
    # see notes above
    if Have_Future():
        # needed for Python 2.3 to support true division
        s = s + "from __future__ import division\n"

    s = s + "if (1/2) == 0: raise Exception('True division does not work')"
    
    return can_run_code(s)

nested_scope_testcode = """
def fff():
    def ggg():
        return ggg

    return ggg()
fff()
"""

def Have_NestedScopes():
    "Does this Python support nested scopes?"
    
    s = ''
    # see notes above
    if Have_Future():
        # needed for Python 2.0 to support nested scopes
        s = s + "from __future__ import nested_scopes\n"
        
    s = s + nested_scope_testcode
    return can_run_code(s)

def Have_Unicode():
    "Does this Python support Unicode strings?"
    return can_run_code("s = u'hello world'")

def Have_StringMethods():
    "Does this Python support string methods? (e.g. ''.lower())"
    return can_run_code("s = ''.lower()")

augassign_test_code = """
i = 1
i += 2
"""

def Have_AugmentedAssignment():
    "Does this Python support augmented assignment ('+=')?"
    return can_run_code(augassign_test_code)

def Have_ListComprehensions():
    "Does this Python support list comprehensions?"
    return can_run_code("l = [x*2 for x in range(1)]")

def Have_ImportAs():
    "Does this Python support 'import module AS name'?"
    # pick a small, Python-only module that exists everywhere
    return can_run_code("import statvfs as abcdefg")

richcomp_test_code = """
class foo:
    def __lt__(self,o):
        return 10

if (foo() < 1) < 10:
    raise Exception # __lt__ wasn't called
"""

def Have_RichComparison():
    "Does this Python support rich comparison methods? (__lt__, etc.)"
    return can_run_code(richcomp_test_code)

funcattr_test_code = """
def f(): pass
f.test = 1
"""

def Have_FunctionAttributes():
    "Does this Python support function attributes?"
    return can_run_code(funcattr_test_code)

def Have_UnifiedLongInts():
    "Does this Python auto-promote ints to longs?"
    return can_run_code("a = 2**64 # becomes a long in Python 2.2+")

def Have_Enumerate():
    "Does this Python support 'enumerate()'?"
    return can_run_code("a = enumerate([1,2,3])")

def Have_ReverseIteration():
    "Does this Python support 'reversed()'?"
    return can_run_code("a = reversed([1,2,3])")

def Have_Basestring():
    "Does this Python support the basestring type?"
    return can_run_code("a = basestring")

def Have_LongRanges():
    "Does this Python support longs (>sys.maxint) in ranges?"
    return can_run_code("range(2**64,2**65,2**64)")

def Have_DictKWArgs():
    "Does this Python support dict() keywords? (i.e. dict(a=1) ==> {'a':1}"
    return can_run_code("dict(a=1,b=2)")

def Have_BuiltinSets():
    "Does this Python have builtin set objects?"
    return can_run_code("set('abcde')")

def Have_GeneratorExpressions():
    "Does this Python support generator expressions?"
    return can_run_code("(x for x in range(1))")

decorator_test_code = """
def foo(f): return f
@foo
def g(): pass
"""

def Have_Decorators():
    "Does this Python support function/method decorators?"
    return can_run_code(decorator_test_code)

multiline_imp_test_code = """
# use same small module as in ImportAs test
from statvfs import (F_BSIZE,
                     F_BLOCKS, F_BFREE,
                     F_FILES)
"""

def Have_MultilineImports():
    "Does this Python support parenthesised multiline imports?"
    return can_run_code(multiline_imp_test_code)

def Have_StringDollarSubst():
    "Does this Python support $-substitution in strings?"
    return can_run_code('from string import Template')

assigndoc_test = """
def f(): pass
f.__doc__ = 'aaa'
"""

def Can_AssignDoc():
    "Old Pythons (pre 1.5?) can't assign to __doc__."
    return can_run_code(assigndoc_test)

#================================================================
#
# Demo showing how to run all the tests.
#
#================================================================

# ugh, Python 1.5 doesn't like '*args' syntax, so do args the ugly way ...

def runtest(msg, test):
    r = test()
    print "%-40s %s" % (msg,['no','yes'][r])

def runtest_1arg(msg, test, arg):
    r = test(arg)
    print "%-40s %s" % (msg,['no','yes'][r])

if __name__ == '__main__':

    import sys,os

    # show banner w/version
    try:
        v = sys.version_info
        print "Python %d.%d.%d-%s [%s, %s]" % (v[0],v[1],v[2],str(v[3]),
                                               os.name,sys.platform)
    except:
        # Python 1.5 lacks sys.version_info
        print "Python %s [%s, %s]" % (string.split(sys.version)[0],
                                      os.name,sys.platform)

    # Python 1.5
    print "			** Python 1.5 features **"
    runtest("Can assign to __doc__?", Can_AssignDoc)
    
    # Python 1.6
    print "			** Python 1.6 features **"
    runtest("Have Unicode?", Have_Unicode)
    runtest("Have string methods?", Have_StringMethods)

    # Python 2.0
    print "			** Python 2.0 features **"	
    runtest("Have augmented assignment?", Have_AugmentedAssignment)
    runtest("Have list comprehensions?", Have_ListComprehensions)
    runtest("Have 'import module AS ...'?", Have_ImportAs)

    # Python 2.1
    print "			** Python 2.1 features **"	
    runtest("Have __future__?", Have_Future)
    runtest("Have rich comparison?", Have_RichComparison)
    runtest("Have function attributes?", Have_FunctionAttributes)
    runtest("Have nested scopes?", Have_NestedScopes)

    # Python 2.2
    print "			** Python 2.2 features **"		
    runtest("Have True/False?", Have_TrueFalse)	
    runtest("Have 'object' type?", Have_ObjectClass)
    runtest("Have __slots__?", Have_Slots)
    # note: can use this to test for existance of any arbitrary module,
    #		I just picked 'compiler' since it showed up in 2.2
    runtest_1arg("Have 'compiler' module?", Have_Module, 'compiler')
    runtest("Have iterators?", Have_Iterators)
    runtest("Have generators?", Have_Generators)
    runtest("Have true division?", Have_TrueDivision)
    runtest("Unified longs/ints?", Have_UnifiedLongInts)
    
    # Python 2.3
    print "		   ** Python 2.3 features **"		
    runtest("Have enumerate()?", Have_Enumerate)
    runtest("Have basestring?", Have_Basestring)
    runtest("Longs > maxint in range()?", Have_LongRanges)
    runtest("dict() accepts keywords?", Have_DictKWArgs)
    runtest("Have 'bool' class?", Have_BoolClass)
    if Have_BoolClass():
        runtest_1arg("bool is a baseclass [expect 'no']?", IsLegal_BaseClass, 'bool')
    
    # Python 2.4
    print "		   ** Python 2.4 features **"		
    runtest("Have builtin sets?", Have_BuiltinSets)
    runtest("Have function/method decorators?", Have_Decorators)
    runtest("Have multiline imports?", Have_MultilineImports)
    runtest("Have generator expressions?", Have_GeneratorExpressions)
    runtest("Have reverse iteration?", Have_ReverseIteration)

    runtest("Have string $-substitution?", Have_StringDollarSubst)

    
