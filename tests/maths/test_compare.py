import numpy as np
import pandas as pd

from arsenal.maths.compare import compare


def test_compare():
    n = 100
    # `a` is a noisy version of `b`, but tends to overestimate.
    a = np.linspace(0, 1, n)
    b = a + np.random.uniform(-0.01, 0.1, size=n)
    compare(a, b)
    compare('a', 'b', data=pd.DataFrame({'a': a, 'b': b}))
