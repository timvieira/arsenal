from __future__ import print_function
import numpy as np
import pylab as pl
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from scipy.linalg import lstsq, norm
from arsenal import colors
from arsenal.iterview import progress
from arsenal.maths.util import cdf, cosine, linf, relative_difference, zero_retrieval
from arsenal import Alphabet


def pp_plot(a, b, pts=100, show_line=True):
    "P-P plot for samples `a` and `b`."
    A = cdf(a)
    B = cdf(b)
    x = np.linspace(min(a.min(), b.min()), max(a.max(), b.max()), pts)

    if show_line:
        pl.plot(range(0,2), range(0,2), ':', alpha=0.5, c='k', lw=2)

    pl.plot(A(x), B(x), alpha=1.0)


def check_equal(expect, got, verbose=0, **kwargs):
    c = compare(expect, got, verbose=verbose, **kwargs)
    if c.max_relative_error > 0.01:
        assert False, c.format_message()
    return c


def align(X, Y, distance=lambda x,y: abs(x - y)):
    """
    Find a cheap alignment of X and Y.
    """
    from scipy.optimize import linear_sum_assignment
    assert len(X) == len(Y)
    n = len(X)
    c = np.zeros((n, n))
    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            c[i,j] = distance(x, y)

    rs,cs = linear_sum_assignment(c)

    class result:
        cost = c[rs,cs].sum()
        x = list(X[r] for r in rs)
        y = list(Y[c] for c in cs)
        x_ind = rs
        y_ind = cs

    return result


class compare(object):

    def __init__(self, expect, got, name=None, data=None, P_LARGER=0.9,
                 regression=True, ax=None, alphabet=None,
                 expect_label=None, got_label=None, verbose=1):
        """Compare vectors.

        Arguments:

          - Specifying data for comparison two methods:

            1) `expect`, `got`: two numeric one-dimensional arrays which we'd like
               to compare (the argument names come for software testing). This
               method requires argument `data=None`.

            2) `data`: instance of `DataFrame`, expects arguments `expect` and `got`
               to be column labels.

          - `name`: name of this comparison.

        Note:

         - when plotting `expect` is the y-axis, `got` is the x-axis. This is by
           convention that `expect` is the dependent variable (regression target).

        TODO:

         - Add an option to drop NaNs and continue comparison.

         - Indicate which dimensions have the largest errors.

         - Add option to allow alignment/matchings?

        """

        self.name = name

        if isinstance(alphabet, Alphabet):
            alphabet = alphabet.tolist()

        if isinstance(expect, dict) and isinstance(got, dict):
            alphabet = list(expect.keys()) if alphabet is None else alphabet
            assert set(got.keys()) == set(alphabet), \
                'Keys differ.\n  got keys  = %s\n  want keys = %s' % (set(got.keys()), set(alphabet))
            expect = [expect[k] for k in alphabet]
            got = [got[k] for k in alphabet]

        if isinstance(expect, np.ndarray) and isinstance(got, np.ndarray):
            assert expect.shape == got.shape, [expect.shape, got.shape]
            expect = expect.flatten()
            got = got.flatten()

        if data is not None:
            assert isinstance(expect, (int, str)), \
                'expected a column name got %s' % type(expect)
            assert isinstance(got, (int, str)), \
                'expected a column name got %s' % type(got)

            if expect_label is None:
                expect_label = expect
            if got_label is None:
                got_label = got

            expect = data[expect]
            got = data[got]

        else:
            if expect_label is None:
                expect_label = 'expect'
            if got_label is None:
                got_label = 'got'

            expect = np.asarray(expect)
            got = np.asarray(got)

            data = pd.DataFrame({expect_label: expect, got_label: got})

        assert expect.shape == got.shape, [expect.shape, got.shape]
        [n] = expect.shape

        self.expect = expect
        self.got = got
        self.alphabet = alphabet
        self.ax = ax
        self.got_label = got_label
        self.expect_label = expect_label
        self.n = n
        self.coeff = None

        self.tests = tests = []

        # Check that vectors are finite.
        if not np.isfinite(expect).all():
            tests.append(['expect finite', progress(np.isfinite(expect).sum(), n), False])
        if not np.isfinite(got).all():
            tests.append(['got finite', progress(np.isfinite(got).sum(), n), False])

        ne = norm(expect)
        ng = norm(got)
        ok = abs(ne-ng)/ne < 0.01 if ne != 0 else True

        if n > 1:
            tests.append(['norms', '[%g, %g]' % (ne, ng), ok])
            F = zero_retrieval(expect, got)
            tests.append(['zero F1', F, F > 0.99])

        if n > 1:
            #self.cosine = cosine(expect, got)
            #tests.append(['cosine', self.cosine, (self.cosine > 0.99999)])   # cosine similarities must be really high.

            self.pearson = 1.0 if ne == ng == 0 else pearsonr(expect, got)[0]
            tests.append(['pearson', self.pearson, (self.pearson > 0.99999)])

            self.spearman = spearmanr(expect, got)[0]
            tests.append(['spearman', self.spearman, (self.spearman > 0.99999)])

        # TODO: this check should probably take into account the scale of the data.
        d = linf(expect, got)
        self.max_err = d
        tests.append(['Linf', d, d < 1e-8])

        # same sign check (weak agreement, but useful sanity check -- especially
        # for gradients)
        x = expect
        y = got
        s = np.asarray(~((x >= 0) ^ (y >= 0)), dtype=int)
        p = s.sum() * 100.0 / len(s)
        tests.append(['same-sign', '%s%% (%s/%s)' % (p, s.sum(), len(s)), p == 100.0])

        # relative error
        r = relative_difference(expect, got)
        r = np.max(r[np.isfinite(r)])
        tests.append(['max rel err', r, r <= 0.01])
        self.max_relative_error = r
        self.max_rel_err = r

        # TODO: suggest that if relative error is high and rescaled error is low (or
        # something to do wtih regression residuals) that maybe there is a
        # (hopefully) simple fix via scale/offset.

        # TODO: can provide descriptive statistics for each vector
        #tests.append(['range (expect)', [expect.min(), expect.max()], 2])
        #tests.append(['range (got)   ', [got.min(), got.max()], 2])

        # regression and rescaled error only valid for n >= 2
        if n >= 2:
            es = abs(expect).max()
            gs = abs(got).max()
            if es == 0:
                es = 1
            if gs == 0:
                gs = 1
            if 0:
                # rescaled error
                E = expect / es
                G = got / gs
                R = abs(E - G)
                r = np.mean(R)
                tests.append(['mean rescaled error', r, r <= 1e-5])

        if regression:
            self.regression()

        if n >= 2:
            # These tests check if one of the datasets is consistently larger than the
            # other. The threshold for error is based on `P_LARGER` ("percent larger").
            L = ((expect-got) > 0).sum()
            if L >= P_LARGER * n:
                tests.append(['expect is larger', progress(L, n), 0])
            L = ((got-expect) > 0).sum()
            if L >= P_LARGER * n:
                tests.append(['got is larger', progress(L, n), 0])

        self.tests = tests
        if verbose:
            self.message()

    def message(self):
        print()
        print(self.format_message())
        print()

    def format_message(self):
        lines = [
            'Comparison%s: n=%s' % (' (%s)' % self.name if self.name else '', self.n),
        ]
        for k, v, passed in self.tests:
            if passed == 1:
                c = colors.green
            elif passed == 0:
                c = colors.red
            else:
                c = colors.yellow
            try:
                v = '%g' % v
            except TypeError:
                pass
            lines.append('  %s: %s' % (k, c % (v,)))
        return '\n'.join(lines)

    def plot(self, regression=True, seaborn=False, ax=None, title=None, name=None, **scatter_kw):
        if ax is not None:
            self.ax = ax

        title = name or self.name or title

        if seaborn:
            import seaborn as sns
            sns.set_context(rc={"figure.figsize": (7, 5)})
            g = sns.JointGrid(self.got_label, self.expect_label, data=self.data)
            g.plot(sns.regplot, sns.distplot, spearmanr)
            print("Pearson's r: {0}".format(self.pearson))
        else:
            if self.ax is None:
                self.ax = pl.figure().add_subplot(111)

            self.ax.scatter(self.got, self.expect, lw=0, alpha=0.5, **scatter_kw)

            self.ax.set_xlabel(self.got_label)
            self.ax.set_ylabel(self.expect_label)

            # Keeps the plot region tight against the data (allow 5% of the
            # data-range for padding so that points in the scatter plot aren't
            # partially clipped.)
            xeps = 0.05 * self.got.ptp()
            self.ax.set_xlim(self.got.min() - xeps, self.got.max() + xeps)

            yeps = 0.05 * self.expect.ptp()
            self.ax.set_ylim(self.expect.min() - yeps, self.expect.max() + yeps)

        if title is not None: self.ax.set_title(title)
        if regression: self.regression_line()
        return self

    def show(self, *args, **kw):
        self.plot(*args, **kw)
        pl.show()
        return self

    def live_plot(self, *args, **kw):
        from arsenal.viz import axman
        name = self.name if self.name is not None else kw.get('name')
        assert name is not None, '`name` required for `live_plot` in order to make the figure.'
        with axman(name) as ax:
            kw['ax'] = ax
            self.plot(*args, **kw)
        return self

    def regression_line(self):
        # TODO: write the coeff to plot.
        if self.coeff is not None and np.isfinite(self.coeff).all():
            xa, xb = self.ax.get_xlim()
            A = np.ones((self.n, 2))
            A[:,0] = self.got
            # plot estimated line
            ys = A.dot(self.coeff)
            self.ax.plot(A[:,0], ys, c='r', alpha=0.5)
            self.ax.grid(True)
            self.ax.set_xlim(xa,xb)
        return self

    def regression(self):
        "least squares linear regression"
        if self.n < 2:
            return
        # data can't contain any NaNs
        if not np.isfinite(self.got).all() or not np.isfinite(self.expect).all():
            self.tests.append(['regression',
                               'did not run due to NaNs in data',
                               0])
            return

        A = np.ones((self.n, 2))
        A[:,0] = self.got

        [self.coeff, _, _, _] = lstsq(A, self.expect)

        # Label with warn or ok.
        ok = 1 if abs(self.coeff - [1, 0]).max() <= 1e-5 else 2

        self.tests.append(['regression', '[%.3f %.3f]' % (self.coeff[0], self.coeff[1]), ok])

    def show_errors(self):
        "show largest relative errors"

        df = []

        def dot_aligned(x):
            sx = [('%g' % s) for s in x]
            dots = [s.find('.') for s in sx]
            m = max(dots)
            y = [' '*(m - d) + s for s, d in zip(sx, dots)]
            z = max(map(len, y))
            fmt = '%%-%ss' % z
            z = [fmt % s for s in y]
            return z

        s_expect = dot_aligned(self.expect)
        s_got = dot_aligned(self.got)

        if self.alphabet is None:
            self.alphabet = range(self.n)

        for (i,(x,y,sx,sy)) in enumerate(zip(self.expect, self.got, s_expect, s_got)):
            # XXX: skip zeros.
            #if abs(x) < 1e-10 and abs(y) < 1e-10:
            #    e = 0.0

            e = relative_difference(x, y)

            if e <= 0.001:
                continue

            df.append([e, self.alphabet[i], x, y, sx, sy])

            #df.append({'name':   alphabet[i],
            #           'error':  e,
            #           'expect': x,
            #           'got':    y})

        df.sort(reverse=1)

        if len(df):
            print(' Largest errors')
            print(' ===============')
            for e, n, x, y, sx, sy in df:

                types = []
                if x < y:
                    types.append('bigger')
                else:
                    types.append('smaller')

                # highlight sign errors.
                #if np.sign(x) != np.sign(y):
                if (x >= 0) != (y >= 0):
                    types.append(colors.red % 'wrong sign')

                print('  %-15s %.2f%%   %s  %s' % (n, e, sx, sy), \
                    ((colors.green % 'ok') if e <= 0.01 else colors.red % 'bad'), \
                    '(%s)' % (', '.join(types)))

        #from pandas import DataFrame
        #df = DataFrame(df)
        #df.set_index('name', inplace=1)
        #print df.sort('error', ascending=0)
        return self


if __name__ == '__main__':

    def test_compare():
        n = 100
        # `a` is a noisy version of `b`, but tends to overestimate.
        a = np.linspace(0,1,n)
        b = a + np.random.uniform(-0.01, 0.1, size=n)
        compare(a,b).show()
        compare('a', 'b', data=pd.DataFrame({'a': a, 'b': b})).show()

        n = 10000
        a = np.random.uniform(-0.1, 0.1, size=n)
        b = np.random.uniform(-0.2, 0.1, size=n)
        pl.figure()
        pp_plot(a, b)
        pl.show()

    test_compare()
