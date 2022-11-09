#!/usr/bin/env python

import os
import sys
import pstats
import cProfile
from arsenal import colors
from contextlib import contextmanager

@contextmanager
def profiler(use='cprofile', filename='out.prof'):

    if use == 'yep':   # pragma: no cover
        import yep
        yep.start(filename)

    if use == 'cprofile':  # pragma: no cover
        #import cProfile
        prof = cProfile.Profile()
        prof.enable()

    try:

        yield

    finally:
        if use == 'yep':  # pragma: no cover
            yep.stop()
            print(colors.yellow % 'wrote: %s' % filename, '(use `google-pprof` to view)')
            # google-pprof --text /bin/ls imitation.prof
            # google-pprof --evince /bin/ls imitation.prof
            # google-pprof --web /bin/ls --web imitation.prof

        if use == 'cprofile':  # pragma: no cover
            #import pstats
            prof.disable()
            prof.dump_stats(filename)
            #pstats.Stats(filename).strip_dirs().sort_stats('time').print_stats()
            print(colors.yellow % 'wrote: %s' % filename, '(use `gprof-viz` to view)')


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


#def kcachegrind(cmd, out='profile.kgrind'):
#    from arsenal.profiling.lsprofcalltree import KCacheGrind
#    p = cProfile.Profile()
#    p.run(cmd)
#    # Get the stats in a form kcachegrind can use and save it
#    k = KCacheGrind(p)
#    with file(out, 'wb') as f:
#        k.output(f)
#    os.system("kcachegrind %s &" % out)


def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.allow_interspersed_args = False
    parser.add_option('-o', '--outfile', dest="outfile",
                      help="Save stats to <outfile>",
                      default='/tmp/profile.tmp')

    if not sys.argv[1:]:
        parser.print_usage()
        sys.exit(2)

    (options, args) = parser.parse_args()

    #viz = kcachegrind
    viz = profile_viz

    sys.path = [os.getcwd()] + sys.path

    if len(args) > 0:
        sys.argv[:] = args
        sys.path.insert(0, os.path.dirname(sys.argv[0]))
        viz('execfile(%r)' % sys.argv[0], out=options.outfile)
    else:
        parser.print_usage()
    return parser


if __name__ == '__main__':
    main()
