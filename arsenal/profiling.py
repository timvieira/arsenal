#!/usr/bin/env python

import os
import sys
import pstats
import cProfile
from arsenal import colors
from contextlib import contextmanager


class profiler:

    def __init__(self, use='cprofile', filename='/tmp/out.prof'):
        self.use = use
        self.filename = filename

    def __enter__(self):
        if self.use == 'yep':   # pragma: no cover
            import yep
            self.prof = yep
            self.prof.start(self.filename)
        if self.use == 'cprofile':  # pragma: no cover
            #import cProfile
            self.prof = cProfile.Profile()
            self.prof.enable()
        return self

    def __exit__(self, *args, **kwargs):
        if self.use == 'yep':  # pragma: no cover
            self.prof.stop()
            print(colors.yellow % 'wrote: %s' % filename, '(use `google-pprof` to view)')
            # google-pprof --text /bin/ls imitation.prof
            # google-pprof --evince /bin/ls imitation.prof
            # google-pprof --web /bin/ls --web imitation.prof
        if self.use == 'cprofile':  # pragma: no cover
            #import pstats
            self.prof.disable()
            self.prof.dump_stats(self.filename)
            #pstats.Stats(filename).strip_dirs().sort_stats('time').print_stats()
            print(colors.yellow % 'wrote: %s' % self.filename, '(use `gprof-viz` to view)')

    def graphviz(self):
        if self.use == 'yep':  # pragma: no cover
            raise NotImplementedError()
        if self.use == 'cprofile':  # pragma: no cover
            return prof_to_graphviz(self.filename)

    def open(self):
        self.graphviz().view()


def prof_to_graphviz(f_prof):
    import gprof2dot
    from graphviz import Source

    f_dot = f_prof + '.dot'

    gprof2dot.main(['-f', 'pstats', '-o', f_dot, f_prof])

    with open(f_dot) as f:
        g = Source(f.read())

    os.remove(f_dot)    # cleanup

    return g


# TODO:
#  - maybe we should delete the `out` tempfile
#  - I don't like that this currently makes a system call to open the image...
#  - gprof2dot is on the pythonpath we should be able to avoid the system call
def profile_viz(
        cmd, global_dict=None,
        local_dict=None,
        img='/tmp/profile.png',
        out='/tmp/profile.tmp',
        noctx=False
):
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


#def main():
#    from optparse import OptionParser
#    parser = OptionParser()
#    parser.allow_interspersed_args = False
#    parser.add_option('-o', '--outfile', dest="outfile",
#                      help="Save stats to <outfile>",
#                      default='/tmp/profile.tmp')
#
#    if not sys.argv[1:]:
#        parser.print_usage()
#        sys.exit(2)
#
#    (options, args) = parser.parse_args()
#
#    #viz = kcachegrind
#    viz = profile_viz
#
#    sys.path = [os.getcwd()] + sys.path
#
#    if len(args) > 0:
#        sys.argv[:] = args
#        sys.path.insert(0, os.path.dirname(sys.argv[0]))
#        viz('execfile(%r)' % sys.argv[0], out=options.outfile)
#    else:
#        parser.print_usage()
#    return parser
#
#
#if __name__ == '__main__':
#    main()


def test_profiler():
    import time

    with profiler() as p:
        for i in range(10):
            time.sleep(.1)

    p.open()


if __name__ == '__main__':
    from arsenal import testing_framework
    testing_framework(globals())
