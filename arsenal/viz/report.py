import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
from collections import defaultdict


class Measurements:
    def __init__(self, colors):
        self.data = {name: defaultdict(list) for name in colors}
        self.colors = colors

    def __call__(self, name, x, samples):
        samples = np.array(samples)
        avg = samples.mean()
        self.data[name]['xs'].append(x)
        self.data[name]['avg'].append(avg)
        if 0:
            std = samples.std()
            hi = avg+std; lo = avg-std
        else:
            hi = np.percentile(samples, 80)
            lo = np.percentile(samples, 20)
        self.data[name]['hi'].append(hi)
        self.data[name]['lo'].append(lo)
        #self.data[name]['samples'].append(samples)

    def show(self, ax=None):
        if ax is None: ax = pl.figure().add_subplot(111)
        # plot all methods +/- error bars.
        for name, data in self.data.items():
            if not data: continue
            df = pd.DataFrame(data)
            pl.fill_between(df['xs'], df.hi, df.lo, alpha=0.1, color=self.colors[name])
            pl.plot(df['xs'], df['avg'], lw=2, c=self.colors[name], alpha=0.5, label=name)
        pl.legend(loc=4, ncol=len(self.data), borderaxespad=0.0, fontsize=10, frameon=0,
                  columnspacing=0.5, handletextpad=0.0)

    def clear(self):
        for d in self.data.values():
            d.clear()
