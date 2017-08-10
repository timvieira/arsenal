from datetime import datetime, timedelta
from copy import deepcopy
from threading import RLock


def timed_cache(seconds=0, minutes=0, hours=0, days=0):

    time_delta = timedelta(seconds=seconds,
                           minutes=minutes,
                           hours=hours,
                           days=days)

    def decorate(f):

        f._lock = RLock()
        f._updates = {}
        f._results = {}

        def do_cache(*args, **kwargs):

            lock = f._lock
            lock.acquire()

            try:
                key = (args, tuple(sorted(kwargs.items(), key=lambda i:i[0])))

                updates = f._updates
                results = f._results

                t = datetime.now()
                updated = updates.get(key, t)

                if key not in results or t-updated > time_delta:
                    # Calculate
                    updates[key] = t
                    result = f(*args, **kwargs)
                    results[key] = deepcopy(result)
                    return result

                else:
                    # Cache
                    return deepcopy(results[key])

            finally:
                lock.release()

        return do_cache

    return decorate


def test_timed_cache():
    import time

    speed = 0.01
    for max_time in [1, 2, 3]:

        class T(object):
            foo = []
            @timed_cache(seconds=max_time * speed)
            def expensive_func(self, c):
                self.foo.append(datetime.now())
                return c

        t = T()
        length = 5
        for _ in xrange(length * max_time):
            time.sleep(speed)
            t.expensive_func(1)

        assert len(t.foo) == length
        for x,y in zip(t.foo, t.foo[1:]):
            diff = (y - x).total_seconds() / speed
            print diff
            assert (diff - max_time) / max_time < 0.1
        print


if __name__ == '__main__':
    test_timed_cache()
