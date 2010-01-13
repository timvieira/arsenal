from __future__ import nested_scopes


## There is still something I don't fully understand here...

import sys

def fmt(s):

    blah = {}
    blah.update(sys._getframe(0).f_builtins)
    blah.update(sys._getframe(0).f_globals)
    blah.update(sys._getframe(0).f_locals)

    k = 0
    success = 0
    while not success or k > 15:
        try:
            fmted = s.format(**blah)
        except KeyError:
            k += 1
            try:
                blah = {}
                for i in reversed(xrange(0, k)):
                    blah.update(sys._getframe(i).f_builtins)
                    blah.update(sys._getframe(i).f_globals)
                    blah.update(sys._getframe(i).f_locals)
            except ValueError:
                raise KeyError('failed formatting string %r.' % s)
        else:
            success = 1
    return fmted


def tests():
    x = 'tests:x'
    y = 'tests:y'
    assert fmt('tests: {x} {y}') == 'tests: tests:x tests:y'
    def foo():
        def goo():
            x = 'goo:x'
            b = 'goo:b'
            def shoo():
                assert fmt('{x}') == 'goo:x'
                assert fmt('{b}') == 'goo:b'
                assert fmt('{b} {x} {y}') == 'goo:b goo:x tests:y'
            assert fmt('{x} {b}') == 'goo:x goo:b'
            shoo()
        assert fmt('{x} {y}') == 'tests:x tests:y'
        goo()
        assert fmt('{x} {y}') == 'tests:x tests:y'
    assert fmt('{x} {y}') == 'tests:x tests:y'
    foo()


tests()
