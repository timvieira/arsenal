import os
import time

from arsenal.profiling import profiler


def test_profiler():
    with profiler() as p:
        for _ in range(10):
            time.sleep(0.01)
    assert os.path.exists(p.filename), 'profile file should be written'
    assert os.path.getsize(p.filename) > 0, 'profile file should be non-empty'

    # Verify the profile data is loadable
    import pstats
    stats = pstats.Stats(p.filename)
    assert stats.total_tt > 0, 'profile should record nonzero total time'
