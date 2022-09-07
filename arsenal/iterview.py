import sys
from time import time

__all__ = ['iterview']


def iterview(
        x: 'Iterable',
        msg: 'Prefix message' = None,
        #mintime: 'show progress at most every `mintime` seconds' = 0.25,
        length: 'length hint; required when len(x) fails.' = None,
        width: 'max width of progress bar' = 78,
        show: 'do not show progress bar if False' = True,
        transient = False,
):

    if not show: return x

    from rich.progress import track
    return track(x,
                 description=msg,
                 disable=not show,
                 transient=transient,
                 total=length)


def progress(n, length):
    """
    Returns a string indicating current progress.
    """
    p = 100 * n / length if length > 0 else 0
    return ('%5.1f%% (%*d/%d)'
            % ((p, len(str(length)), n, length)))


#def progress_bar(max_width, n, length):
#    """
#    Returns a progress bar (string).
#
#    Arguments:
#
#    max_width -- maximum width of the progress bar
#    """
#
#    width = int((float(n) / length) * max_width + 0.5) # at least one
#
#    if max_width - width:
#        spacing = '>' + (' ' * (max_width - width))[1:]
#    else:
#        spacing = ''
#
#    return '[%s%s]' % ('=' * width, spacing)
#
#
#def time_remaining(elapsed, n, length):
#    """
#    Returns a string indicating the time remaining (if not complete)
#    or the total time elapsed (if complete).
#    """
#
#    if n == 0:
#        return '--:--:--'
#
#    if n == length:
#        seconds = int(elapsed) # if complete, total time elapsed
#    else:
#        seconds = int((elapsed / n) * (length - n)) # otherwise, time remaining
#
#    minutes, seconds = divmod(seconds, 60)
#    hours, minutes = divmod(minutes, 60)
#
#    return '%02d:%02d:%02d' % (hours, minutes, seconds)
#
#
#def time_elapsed(elapsed):
#    """
#    Returns a string indicating the time elapsed.
#    """
#
#    seconds = int(elapsed) # if complete, total time elapsed
#    minutes, seconds = divmod(seconds, 60)
#    hours, minutes = divmod(minutes, 60)
#
#    return '%02d:%02d:%02d' % (hours, minutes, seconds)
#

#def fmt(start, n, length, width, done=False):
#    """
#    returns ...
#    """
#
#    string = progress(n, length) + ' ' # current progress
#
#    if n == length or done:
#        end = ' '
#    else:
#        end = ' ETA '
#
#    if done:
#        end += time_elapsed(time() - start)
#    else:
#        end += time_remaining(time() - start, n, length)
#
#    string += progress_bar(width - len(string) - len(end), n, length)
#    string += end
#
#    return string
#
#
#def _iterview(
#        x: 'Iterable',
#        msg: 'Prefix message' = None,
#        mintime: 'show progress at most every `mintime` seconds' = 0.25,
#        length: 'length hint; required when len(x) fails.' = None,
#        width: 'max width of progress bar' = 78,
#        show: 'do not show progress bar if False' = True
#):
#    """
#    Show a progress bar as we move through the iterable `x`.
#
#    >>> for i in iterview(range(10000), msg='foo'): pass
#    foo  20.0% ( 2001/10000) [=========>                                  ] 00:00:02
#
#    """
#
#    if not show:
#        yield from x
#
#    else:
#        start = time()
#
#        if length is None:
#            try:
#                length = len(x)
#            except TypeError:
#                raise TypeError(f'Iterable `{x!r}` does not have a known length.\n'
#                                'Please provide in an `x` where `len(x)` is defined '
#                                'or explicitly provide a value in the `length` argument.')
#        else:
#            length = int(length)
#
#        if length == 0:
#            return
#
#        n = 0
#        if msg:
#            assert len(msg) + 1 <= width, 'msg too wide'
#            width = width - len(msg) - 1
#            msg = msg + ' '
#        else:
#            msg = ''
#
#        last_update = 0
#
#        try:
#            for n, y in enumerate(x):
#                if not mintime or time() - last_update >= mintime:
#                    sys.stderr.write('\r%s%s' % (msg, fmt(start, n, length, width)))
#                    last_update = time()
#                yield y
#        finally:
#            sys.stderr.write('\r%s%s\n' % (msg, fmt(start, n+1, length, width, done=1)))


def tests():
    from arsenal.assertions import assert_throws
    from time import sleep

    # Check for error
    with assert_throws(ValueError):
        list(iterview((None for _ in range(5))))

    # won't throw an error because length is passed in
    list(iterview((None for _ in range(5)), length=5))

    for _ in iterview(range(10000), msg='foo', mintime=0.25):
        sleep(0.0001)

    # Print time elapsed if we terminate earlier than expected.
    for i in iterview(range(10000), msg='foo', mintime=0.25):
        if i == 2000: break
        sleep(0.001)

    from arsenal import terminal
    print('should disappear', terminal.arrow.down)
    # Print time elapsed if we terminate earlier than expected.
    for i in iterview(range(10000), msg='foo', mintime=0.25, transient=True):
        if i == 2000: break
        sleep(0.001)
    print('should disappear', terminal.arrow.up)



if __name__ == '__main__':
    tests()
