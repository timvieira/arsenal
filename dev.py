#!/usr/bin/env python

# TODO: 
#  * Is there a way to remove the topmost level traceback's which correspond to
#    this script?

import sys

from debug import ultraTB2

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--coverage',action="store_true", default=False)
parser.add_option('--doctest', action="store_true", default=False)
parser.add_option('--verbose-doctest', action="store_true", default=False)
parser.add_option('--pm', action="store_true", default=False)
parser.add_option('--breakin', action="store_true", default=False)
parser.add_option('--automain', action="store_true", default=False)
parser.add_option('--less-verbose', action="store_true", default=False)

# split the argument list at the first item ending with .py
source = [(i+1,f) for i, f in enumerate(sys.argv[1:]) if f.endswith('.py')]

devargs = sys.argv[:source[0][0]]
scriptargs = sys.argv[source[0][0]:]

#print 'devargs:', devargs
#print 'scriptargs:',  scriptargs

(opts, args) = parser.parse_args(devargs)

if opts.less_verbose:
    ultraTB2.enable(include_vars=False)
else:
    ultraTB2.enable()

# hack sys.argv so that it no longer contains this script's options
sys.argv = scriptargs

if opts.coverage:
    from coverage import coverage
    cov = coverage(data_suffix=True, branch=True)
    cov.start()

if opts.doctest or opts.verbose_doctest:
    import doctest, atexit
    if opts.verbose_doctest:
        atexit.register(lambda: doctest.testmod(verbose=True))
    else:
        if opts.doctest:
            atexit.register(doctest.testmod)

if opts.pm:
    from debug.utils import enable_pm
    enable_pm()

if opts.breakin:
    from debug import breakin
    breakin.enable()

# execute the file
execfile(source[0][1])

if opts.automain:
    from automain import automain
    automain()


