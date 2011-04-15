#!/usr/bin/env python

import os
import sys
import pstats
import cProfile
import tempfile

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


if __name__ == '__main__':
    viz = profile_viz
    if '--kgrind' in sys.argv:
        viz = kcachegrind
        sys.argv.remove('--kgrind')  # hack sys.argv
    if len(sys.argv) > 1:
        sys.argv.pop(0)  # hack sys.argv
        viz('execfile(%r)' % sys.argv[0])
