from datetime import datetime, timedelta
from time import time, localtime, strftime
import atexit


# TODO: option to use terminal width if possible
def marquee(txt='', width=78, mark='*'):
    """
    Return the input string centered in a 'marquee'.

    >>> marquee('hello', width=50)
    '********************* hello *********************'
    """
    if not txt:
        return (mark*width)[:width]
    nmark = int((width-len(txt)-2)/len(mark)/2)
    if nmark < 0: nmark =0
    marks = mark*nmark
    return '%s %s %s' % (marks, txt, marks)


def nth(n):
    """
    Formats an ordinal.
    Doesn't handle negative numbers.

    >>> nth(1)
    '1st'
    >>> nth(0)
    '0th'
    >>> [nth(x) for x in [2, 3, 4, 5, 10, 11, 12, 13, 14]]
    ['2nd', '3rd', '4th', '5th', '10th', '11th', '12th', '13th', '14th']
    >>> [nth(x) for x in [91, 92, 93, 94, 99, 100, 101, 102]]
    ['91st', '92nd', '93rd', '94th', '99th', '100th', '101st', '102nd']
    >>> [nth(x) for x in [111, 112, 113, 114, 115]]
    ['111th', '112th', '113th', '114th', '115th']
    """
    assert n >= 0
    if n % 100 in [11, 12, 13]:
        return '%sth' % n
    return {1: '%sst', 2: '%snd', 3: '%srd'}.get(n % 10, '%sth') % n


def timetuple(s):
    "htime(x) -> (days, hours, minutes, seconds)"
    s = int(s)
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return (d, h, m, s)


def htime(s, show_seconds=True):
    """Given a number of seconds, returns a string attempting to represent
    it as shortly as possible.
    >>> htime(100000)
    '1d3h46m40s'
    >>> htime(1)
    '1s'
    >>> htime(10)
    '10s'
    >>> htime(1000)
    '16m40s'
    >>> htime(10000)
    '2h46m40s'
    """
    (d, h, m, s) = timetuple(s)
    x = []
    if d:
        x.append('%sd' % d)
    if h:
        x.append('%sh' % h)
    if m:
        x.append('%sm' % m)
    if show_seconds and s:
        x.append('%ss' % s)
    if not x:
        if show_seconds:
            x = ['%ss' % s]
        else:
            x = ['0m']
    return ''.join(x)


def datestr(then, now=None):
    """
    Converts a (UTC) datetime object to a nice string representation.

    >>> d = datetime(1970, 5, 1)
    >>> datestr(d, now=d)
    '0 microseconds ago'
    >>> datestr(datetime(1970, 1, 1), now=d)
    'Jan 01'
    >>> datestr(datetime(1969, 1, 1), now=d)
    'Jan 01, 1969'
    >>> datestr(datetime(1970, 6, 1), now=d)
    'Jun 01, 1970'
    >>> datestr(None)
    ''
    """

    def agohence(n, what, divisor=None):
        if divisor:
            n //= divisor
        out = str(abs(n)) + ' ' + what       # '2 day'
        if abs(n) != 1:
            out += 's'                       # '2 days'
        out += ' '                           # '2 days '
        if n < 0:
            out += 'from now'
        else:
            out += 'ago'
        return out                           # '2 days ago'

    oneday = 24 * 60 * 60

    if not then:
        return ""
    if not now:
        now = datetime.now()

    delta = now - then
    deltaseconds = int(delta.total_seconds())
    deltadays = abs(deltaseconds) // oneday
    if deltaseconds < 0:
        deltadays *= -1 # fix for oddity of floor

    if deltadays:
        if abs(deltadays) < 4:
            return agohence(deltadays, 'day')

        out = then.strftime('%b %d') # e.g. 'June 13'
        if then.year != now.year or deltadays < 0:
            out += ', %s' % then.year
        return out

    if int(deltaseconds):
        if abs(deltaseconds) > (60 * 60):
            return agohence(deltaseconds, 'hour', 60 * 60)
        elif abs(deltaseconds) > 60:
            return agohence(deltaseconds, 'minute', 60)
        else:
            return agohence(deltaseconds, 'second')

    deltamicroseconds = delta.microseconds
    if delta.days:
        deltamicroseconds = int(delta.microseconds - 1e6) # datetime oddity
    if abs(deltamicroseconds) > 1000:
        return agohence(deltamicroseconds, 'millisecond', 1000)

    return agohence(deltamicroseconds, 'microsecond')


# TODO: use htime and marquee
def print_elapsed_time():
    "register an exit hook which prints the start, finish, and elapsed times of a script."
    begin = time()
    started = localtime()
    def hook():
        secs = time() - begin
        mins, secs = divmod(secs, 60)
        hrs, mins = divmod(mins, 60)
        print()
        print('======================================================================')
        print('Started on', strftime("%B %d, %Y at %I:%M:%S %p", started))
        print('Finished on', strftime("%B %d, %Y at %I:%M:%S %p", localtime()))
        print('Total time: %02d:%02d:%02d' % (hrs, mins, secs))
        print()
    atexit.register(hook)


# borrowed from girzzled https://github.com/bmc/grizzled-python/blob/master/grizzled/text/__init__.py
def str2bool(s):
    """
    Convert a string to a boolean value. The supported conversions are:

        +--------------+---------------+
        | String       | Boolean value |
        +==============+===============+
        | "false"      | False         |
        +--------------+---------------+
        | "true"       | True          |
        +--------------+---------------+
        | "f"          | False         |
        +--------------+---------------+
        | "t"          + True          |
        +--------------+---------------+
        | "0"          | False         |
        +--------------+---------------+
        | "1"          + True          |
        +--------------+---------------+
        | "n"          | False         |
        +--------------+---------------+
        | "y"          + True          |
        +--------------+---------------+
        | "no"         | False         |
        +--------------+---------------+
        | "yes"        + True          |
        +--------------+---------------+
        | "off"        | False         |
        +--------------+---------------+
        | "on"         + True          |
        +--------------+---------------+

    Strings are compared in a case-blind fashion.

    **Note**: This function is not currently localizable.

    :Parameters:
        s : str
            The string to convert to boolean

    :rtype: bool
    :return: the corresponding boolean value

    :raise ValueError: unrecognized boolean string
    """
    try:
        return {
            'true' : True,  'false': False,
            't'    : True,  'f'    : False,
            '1'    : True,  '0'    : False,
            'yes'  : True,  'no'   : False,
            'y'    : True,  'n'    : False,
            'on'   : True,  'off'  : False,
        }[s.lower()]
    except KeyError:
        raise ValueError('Unrecognized boolean string: "%s"' % s)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    def test():
        d = datetime(1970, 5, 1)

        examples = {
            timedelta(microseconds=1): '1 microsecond ago',
            timedelta(microseconds=2): '2 microseconds ago',
            -timedelta(microseconds=1): '1 microsecond from now',
            -timedelta(microseconds=2): '2 microseconds from now',
            timedelta(microseconds=2000): '2 milliseconds ago',
            timedelta(seconds=2): '2 seconds ago',
            timedelta(seconds=2*60): '2 minutes ago',
            timedelta(seconds=2*60*60): '2 hours ago',
            timedelta(days=2): '2 days ago',
        }

        for t, v in list(examples.items()):
            assert datestr(d, now=d+t) == v

    test()
