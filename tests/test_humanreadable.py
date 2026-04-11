from datetime import datetime, timedelta

from arsenal.humanreadable import datestr


def test_datestr():
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
