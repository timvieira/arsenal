"""
I've recently needed to profile some very subtle issues that cropped up in a customer's python
application. However, when I tried to use hotshot, I consistently got tracebacks. After some 
digging around on the net, I saw folks saying that profiling is basically busted in python2.4 
(and then I remembered Itamar saying basically the same thing at PyCon 2006 when we were looking 
at web2 slowness).

To get around this, I built python2.5 from svn and copied its cProfile, _lsprof and pstats files 
to my python2.4 libs. This was a complete desperation move and I totally didn't expect it to work --
but it did (with only a warning about a version mismatch).

Earlier this year, JP and Itamar updated an lsprof patch to work as a standalone. However, I've
never done any profiling in python, so it took a few minutes to get up to speed. Looking at the
patch source and the python2.5 cProfile docs and then doing the usual dir() and help() on
cProfile.Profile in the python interpreter is what helped the most.

To give others new to profiling a jumpstart, I'm including a quick little toy howto below.

Import the junk:
"""

import os
import cProfile
import lsprofcalltree

def myFunc():
    myPath = os.path.expanduser('~/timv')
    print "Hello, world! This is my home:"
    print myPath

# Define a profile object and run it:
p = cProfile.Profile()
p.run('myFunc()')

# Get the stats in a form kcachegrind can use and save it:
k = lsprofcalltree.KCacheGrind(p)

with file('prof.kgrind', 'w+') as f:
    k.output(f)

"""
You can now open up the prof.kgrind file in kcachegrind and view the (in this case, 
very uninteresting) results to your heart's content.
"""

os.system("kcachegrind prof.kgrind &")

