import hotshot, hotshot.stats, tempfile
import time
from cStringIO import StringIO

# TODO: this will be a good module to include an easy api for the visualization
# stuff like gprof2dot.py, pyprof2calltree.py

def profile(f, *args, **kw):
    """
    Profiles function `f` and returns a tuple containing its output
    and a string with human-readable profiling information.
    """
    temp = tempfile.NamedTemporaryFile()
    prof = hotshot.Profile(temp.name)

    stime = time.time()
    result = prof.runcall(f, *args, **kw)
    stime = time.time() - stime
    prof.close()

    out = StringIO()
    stats = hotshot.stats.load(temp.name)
    stats.stream = out
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    stats.print_stats()
    stats.print_callers()

    x =  '\n\ntook '+ str(stime) + ' seconds\n'
    x += out.getvalue()

    return (result, x)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    out, info = profile(time.sleep, 0.01)
    print info
