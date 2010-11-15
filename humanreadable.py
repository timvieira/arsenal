import datetime

def nthstr(n):
    """
    Formats an ordinal.
    Doesn't handle negative numbers.

    >>> nthstr(1)
    '1st'
    >>> nthstr(0)
    '0th'
    >>> [nthstr(x) for x in [2, 3, 4, 5, 10, 11, 12, 13, 14, 15]]
    ['2nd', '3rd', '4th', '5th', '10th', '11th', '12th', '13th', '14th', '15th']
    >>> [nthstr(x) for x in [91, 92, 93, 94, 99, 100, 101, 102]]
    ['91st', '92nd', '93rd', '94th', '99th', '100th', '101st', '102nd']
    >>> [nthstr(x) for x in [111, 112, 113, 114, 115]]
    ['111th', '112th', '113th', '114th', '115th']
    """    
    assert n >= 0
    if n % 100 in [11, 12, 13]: return '%sth' % n
    return {1: '%sst', 2: '%snd', 3: '%srd'}.get(n % 10, '%sth') % n


def htime(s):
    """htime(x) -> (days, hours, min, seconds)"""
    m, s = divmod(s, 60)
    h, m = divmod(min, 60)
    d, h = divmod(h, 24)
    return int(d), int(h), int(m), s

def sec2prettytime(diff, show_seconds=True):
    """Given a number of seconds, returns a string attempting to represent
    it as shortly as possible.

    >>> sec2prettytime(100000)
    '1d3h46m40s'
    """
    diff = int(diff)
    days, diff = divmod(diff, 86400)
    hours, diff = divmod(diff, 3600)
    minutes, seconds = divmod(diff, 60)
    x = []
    if days:
        x.append('%sd' % days)
    if hours:
        x.append('%sh' % hours)
    if minutes:
        x.append('%sm' % minutes)
    if show_seconds and seconds:
        x.append('%ss' % seconds)
    if not x:
        if show_seconds:
            x = ['%ss' % seconds]
        else:
            x = ['0m']
    return ''.join(x)



def datestr(then, now=None):
    """
    Converts a (UTC) datetime object to a nice string representation.
    
        >>> from datetime import datetime, timedelta
        >>> d = datetime(1970, 5, 1)
        >>> datestr(d, now=d)
        '0 microseconds ago'
        >>> for t, v in {
        ...   timedelta(microseconds=1): '1 microsecond ago',
        ...   timedelta(microseconds=2): '2 microseconds ago',
        ...   -timedelta(microseconds=1): '1 microsecond from now',
        ...   -timedelta(microseconds=2): '2 microseconds from now',
        ...   timedelta(microseconds=2000): '2 milliseconds ago',
        ...   timedelta(seconds=2): '2 seconds ago',
        ...   timedelta(seconds=2*60): '2 minutes ago',
        ...   timedelta(seconds=2*60*60): '2 hours ago',
        ...   timedelta(days=2): '2 days ago',
        ... }.iteritems():
        ...     assert datestr(d, now=d+t) == v
        >>> datestr(datetime(1970, 1, 1), now=d)
        'January  1'
        >>> datestr(datetime(1969, 1, 1), now=d)
        'January  1, 1969'
        >>> datestr(datetime(1970, 6, 1), now=d)
        'June  1, 1970'
        >>> datestr(None)
        ''
    """
    def agohence(n, what, divisor=None):
        if divisor: n = n // divisor

        out = str(abs(n)) + ' ' + what       # '2 day'
        if abs(n) != 1: out += 's'           # '2 days'
        out += ' '                           # '2 days '
        if n < 0:
            out += 'from now'
        else:
            out += 'ago'
        return out                           # '2 days ago'

    oneday = 24 * 60 * 60

    if not then: return ""
    if not now: now = datetime.datetime.utcnow()
    if type(now).__name__ == "DateTime":
        now = datetime.datetime.fromtimestamp(now)
    if type(then).__name__ == "DateTime":
        then = datetime.datetime.fromtimestamp(then)
    elif type(then).__name__ == "date":
        then = datetime.datetime(then.year, then.month, then.day)

    delta = now - then
    deltaseconds = int(delta.days * oneday + delta.seconds + delta.microseconds * 1e-06)
    deltadays = abs(deltaseconds) // oneday
    if deltaseconds < 0: deltadays *= -1 # fix for oddity of floor

    if deltadays:
        if abs(deltadays) < 4:
            return agohence(deltadays, 'day')

        out = then.strftime('%B %e') # e.g. 'June 13'
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
    if delta.days: deltamicroseconds = int(delta.microseconds - 1e6) # datetime oddity
    if abs(deltamicroseconds) > 1000:
        return agohence(deltamicroseconds, 'millisecond', 1000)

    return agohence(deltamicroseconds, 'microsecond')



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    doctest.run_docstring_examples("""
    >>> sec2prettytime(1)
    '1s'
    >>> sec2prettytime(10)
    '10s'
    >>> sec2prettytime(100)
    '1m40s'
    >>> sec2prettytime(60)
    '1m'
    >>> sec2prettytime(1000)
    '16m40s'
    >>> sec2prettytime(10000)
    '2h46m40s'
    """, globals(), verbose=0)

