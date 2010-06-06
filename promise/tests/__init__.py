
import os
import sys
import timeit
import unittest

import promise
import dis
from promise.byteplay import *


class TestPromiseTiming(unittest.TestCase):
    """Run timing tests for suitable sub-modules.

    This class finds all sub-modules of promise.tests and tries to load each
    of them as a timing test.  A module named 'testmod' must define a function
    'verify' and a series of functions 'testmod0', 'testmod1' etc.  The verify
    function will be called with each of the testmodX functions in order, and
    we assert that each is successively faster than its predecessor.
    """

    def _timeit(self,modnm,funcnms,funcnm):
        setup = "from promise.tests.%s import verify, %s; " % (modnm,funcnms)
        setup += "verify(%s)" % (funcnm,) # run once to apply deferred promises
        if "PROMISE_SKIP_TIMING_TESTS" in os.environ:
            num = 2
        else:
            num = 100000
        ts = timeit.Timer("verify(%s)"%(funcnm,),setup).repeat(number=num)
        if "PROMISE_SKIP_TIMING_TESTS" not in os.environ:
            print funcnm, sorted(ts)
        return min(ts)

    def _make_test(modnm):
        """Make a timing test method from the given module name."""
        def test(self):
            if "PROMISE_SKIP_TIMING_TESTS" not in os.environ:
                sys.stderr.write("running timing test for '%s', please wait\n" % (modnm,))
            mod = getattr(__import__("promise.tests."+modnm).tests,modnm)
            funcs = []
            for funcnm in dir(mod):
                if funcnm.startswith(modnm):
                   funcs.append(funcnm)
            funcs.sort()
            funcnms = ",".join(funcs)
            t0 = self._timeit(modnm,funcnms,funcs[0])
            for funcnm in funcs[1:]:
                t1 = self._timeit(modnm,funcnms,funcnm)
                if "PROMISE_SKIP_TIMING_TESTS" not in os.environ:
                    self.assertTrue(t0 > t1)
                t0 = t1
        test.__name__ = "test_" + modnm
        return test

    for modnm in os.listdir(os.path.dirname(__file__)):
        if modnm.endswith(".py") and modnm != "__init__.py":
            nm = modnm[:-3]
            locals()["test_"+nm] = _make_test(nm)


def test_inlining():
    """Test that function inlining works under a variety of circumstances."""
    @promise.pure()
    def calc(a,b=7):
        return 2*a + 3*b
    items = [(1,7),(3,7),(5,7)]
    #  Version using list comprehension produces a for-loop
    def aggregate0(items):
        return sum([calc(a,b) for (a,b) in items])
    assert (LOAD_DEREF,"calc") in Code.from_code(aggregate0.func_code).code
    assert (BINARY_ADD,None) not in Code.from_code(aggregate0.func_code).code
    #  Version using generator comprehension produces a closure
    def aggregate1(items):
        return sum(calc(a,b) for (a,b) in items)
    assert aggregate0(items) == aggregate1(items)
    genexp = aggregate1.func_code.co_consts[1]
    assert (LOAD_DEREF,"calc") in Code.from_code(genexp).code
    assert (BINARY_ADD,None) not in Code.from_code(genexp).code
    #  Pure function can be folded into the for-loop
    @promise.constant(["calc"])
    def aggregate2(items):
        return sum([calc(a,b) for (a,b) in items])
    assert aggregate0(items) == aggregate2(items)
    assert (LOAD_DEREF,"calc") not in Code.from_code(aggregate2.func_code).code
    assert (BINARY_ADD,None) in Code.from_code(aggregate2.func_code).code
    #  Pure function can be pushed inside closure
    @promise.constant(["calc"])
    def aggregate3(items):
        return sum(calc(a,b) for (a,b) in items)
    assert aggregate0(items) == aggregate3(items)
    genexp = aggregate3.func_code.co_consts[1]
    assert (LOAD_DEREF,"calc") not in Code.from_code(genexp).code
    assert (BINARY_ADD,None) in Code.from_code(genexp).code
    #  Default arguments are respected
    @promise.constant(["calc"])
    def aggregate4(items):
        return sum(calc(a) for (a,_) in items)
    assert aggregate0(items) == aggregate4(items)
    genexp = aggregate4.func_code.co_consts[1]
    assert (LOAD_DEREF,"calc") not in Code.from_code(genexp).code
    assert (BINARY_ADD,None) in Code.from_code(genexp).code
    
    

def test_README():
    """Ensure that the README is in sync with the docstring.

    This test should always pass; if the README is out of sync it just updates
    it with the contents of promise.__doc__.
    """
    dirname = os.path.dirname
    readme = os.path.join(dirname(dirname(dirname(__file__))),"README.txt")
    if not os.path.isfile(readme):
        f = open(readme,"wb")
        f.write(promise.__doc__)
        f.close()
    else:
        f = open(readme,"rb")
        if f.read() != promise.__doc__:
            f.close()
            f = open(readme,"wb")
            f.write(promise.__doc__)
            f.close()

