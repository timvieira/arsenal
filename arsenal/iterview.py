import sys
from time import time

__all__ = ['iterview']


def progress(n, length):
    """
    Returns a string indicating current progress.
    """

    return ('%5.1f%% (%*d/%d)'
            % ((float(n) / length) * 100, len(str(length)), n, length))


def progress_bar(max_width, n, length):
    """
    Returns a progress bar (string).

    Arguments:

    max_width -- maximum width of the progress bar
    """

    width = int((float(n) / length) * max_width + 0.5) # at least one

    if max_width - width:
        spacing = '>' + (' ' * (max_width - width))[1:]
    else:
        spacing = ''

    return '[%s%s]' % ('=' * width, spacing)


def time_remaining(elapsed, n, length):
    """
    Returns a string indicating the time remaining (if not complete)
    or the total time elapsed (if complete).
    """

    if n == 0:
        return '--:--:--'

    if n == length:
        seconds = int(elapsed) # if complete, total time elapsed
    else:
        seconds = int((elapsed / n) * (length - n)) # otherwise, time remaining

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return '%02d:%02d:%02d' % (hours, minutes, seconds)


def fmt(start, n, length, width):
    """
    returns ...
    """

    string = progress(n, length) + ' ' # current progress

    if n == length:
        end = ' '
    else:
        end = ' ETA '

    end += time_remaining(time() - start, n, length)

    string += progress_bar(width - len(string) - len(end), n, length)
    string += end

    return string


def iterview(x, msg=None, every=10, mintime=None, length=None, width=78):
    """
    Returns an iterator which prints its progress to stderr.

    Arguments:

      x: iterator

      every: number of iterations between printing progress

      length: hint about the length of x, which is required when generators has
          unknown `len()`.

      mintime: show progress at most every `mintime` seconds.

    """

    start = time()
    length = length or len(x)

    if length == 0:
        raise StopIteration

    n = 0
    if msg:
        assert len(msg) + 1 <= width, 'msg too wide'
        width = width - len(msg) - 1
        msg = msg + ' '
    else:
        msg = ''

    last_update = 0

    for n, y in enumerate(x):
        if every is None or n % every == 0:
            if not mintime or time() - last_update >= mintime:
                sys.stderr.write('\r%s%s' % (msg, fmt(start, n, length, width)))
                last_update = time()

        yield y

    sys.stderr.write('\r%s%s\n' % (msg, fmt(start, n+1, length, width)))


if __name__ == '__main__':
    from time import sleep

    for _ in iterview(xrange(400), every=20):
        sleep(0.005)

    for _ in iterview(xrange(10000), msg='foo', mintime=0.25):
        sleep(0.001)
