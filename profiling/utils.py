#!/usr/bin/env python

import os
import sys
import pstats
import cProfile

# TODO: 
#  - maybe we should delete the `out` tempfile
#  - I don't like that this currently makes a system call to open the image...
#  - gprof2dot is on the pythonpath we should be able to avoid the system call
def profile_viz(cmd, global_dict=None, local_dict=None, img='profile.png', out='profile.tmp', noctx=False):
    "Run gprof2dot on the output for profiling."
    if noctx:
        cProfile.run(cmd, out)
    else:
        if local_dict is None and global_dict is None:
            call_frame = sys._getframe().f_back
            local_dict = call_frame.f_locals
            global_dict = call_frame.f_globals
        cProfile.runctx(cmd, global_dict, local_dict, out)

    stats = pstats.Stats(out)
    stats.strip_dirs()               # Clean up filenames for the report
    stats.sort_stats('cumulative')   # sort by the cumulative time
    stats.print_stats()
    # for more on the viz check out: http://code.google.com/p/jrfonseca/wiki/Gprof2Dot
    os.system('gprof2dot.py -f pstats %s | dot -Tpng -o %s && eog %s &' % (out, img, img))


def kcachegrind(cmd, out='profile.kgrind'):
    from profiling.lsprofcalltree import KCacheGrind
    p = cProfile.Profile()
    p.run(cmd)
    # Get the stats in a form kcachegrind can use and save it
    k = KCacheGrind(p)
    with file(out, 'wb') as f:
        k.output(f)
    os.system("kcachegrind %s &" % out)


## from cStringIO import StringIO
## import time, hotshot, hotshot.stats, tempfile
## def profile(f, *args, **kw):
##     """
##     Profiles function `f` and returns a tuple containing its output
##     and a string with human-readable profiling information.
##     """
##     temp = tempfile.NamedTemporaryFile()
##     prof = hotshot.Profile(temp.name)
##
##     stime = time.time()
##     result = prof.runcall(f, *args, **kw)
##     stime = time.time() - stime
##     prof.close()
##
##     out = StringIO()
##     stats = hotshot.stats.load(temp.name)
##     stats.stream = out
##     stats.strip_dirs()
##     stats.sort_stats('time', 'calls')
##     stats.print_stats()
##     stats.print_callers()
##
##     x =  '\n\ntook '+ str(stime) + ' seconds\n'
##     x += out.getvalue()
##
##     return (result, x)


