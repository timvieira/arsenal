#!/usr/bin/env python

import os
import sys
import pstats
import cProfile

# maybe add an option to delete `out` tempfile or keep it
# I don't like that this currently makes a system call to open the image...
# gprof2dot is on the pythonpath we should be able to avoid the system call there
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


def main():
    from optparse import OptionParser

    parser = OptionParser()
    parser.allow_interspersed_args = False
    parser.add_option('-i', '--img', dest="image", help="Save image of hotspots to <img>", default='profile.png')
    parser.add_option('-o', '--out', dest="out", help="Save stats to <outfile>", default='profile.tmp')

    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(2)

    (options, args) = parser.parse_args()

    if len(args) > 0:
        sys.argv[:] = args
        sys.path.insert(0, os.path.dirname(sys.argv[0]))
        profile_viz('execfile(%r)' % (sys.argv[0],), img=options.image, out=options.out, noctx=True)
    else:
        parser.print_help()
    return parser


if __name__ == '__main__':
    #print profile(time.sleep, 0.01)[1]
    main()
