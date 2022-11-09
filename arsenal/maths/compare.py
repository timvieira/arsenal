import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from scipy.linalg import lstsq, norm
from arsenal import colors
from arsenal.iterview import progress
from arsenal.maths import cosine, linf, relative_difference, zero_retrieval
from arsenal.maths.rvs import cdf
from arsenal import Alphabet


def pp_plot(a, b, pts=100, show_line=True):
    "P-P plot for samples `a` and `b`."
    A = cdf(a)
    B = cdf(b)
    x = np.linspace(min(a.min(), b.min()), max(a.max(), b.max()), pts)

    if show_line:
        pl.plot(range(0,2), range(0,2), ':', alpha=0.5, c='k', lw=2)

    pl.plot(A(x), B(x), alpha=1.0)


def check_equal(want, have, verbose=0, **kwargs):
    c = compare(want, have, verbose=verbose, **kwargs)
    if c.max_relative_error > 0.01:
        assert False, c.format_message()
    return c


def align(X, Y, distance=lambda x,y: abs(x - y), maximize=False):
    """
    Find a cheap alignment of X and Y.
    """
    from scipy.optimize import linear_sum_assignment
    n = len(X); m = len(Y)
    c = np.zeros((n, m))
    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            c[i,j] = distance(x, y)

    rs,cs = linear_sum_assignment(c, maximize=maximize)

    class result:
        cost = c[rs,cs].sum()
        x = list(X[r] for r in rs)
        y = list(Y[c] for c in cs)
        x_ind = rs
        y_ind = cs
        cost_matrix = c

    return result


class compare:

    def __init__(self, want, have, name=None, data=None, P_LARGER=0.9,
                 regression=True, ax=None, alphabet=None,
                 want_label=None, have_label=None, verbose=1):
        """Compare vectors.

        Arguments:

          - Specifying data for comparison two methods:

            1) `want`, `have`: two numeric one-dimensional arrays which we'd like
               to compare (the argument names come for software testing). This
               method requires argument `data=None`.

            2) `data`: instance of `DataFrame`, expects arguments `want` and `have`
               to be column labels.

          - `name`: name of this comparison.

        Note:

         - when plotting `want` is the y-axis, `have` is the x-axis. This is by
           convention that `want` is the dependent variable (regression target).

        TODO:

         - Add an option to drop NaNs and continue comparison.

         - Indicate which dimensions have the largest errors.

         - Add option to allow alignment/matchings?

        """

        self.name = name

        if isinstance(alphabet, Alphabet):
            alphabet = list(alphabet)

        if isinstance(want, dict) and isinstance(have, dict):
            alphabet = list(want.keys() | have.keys()) if alphabet is None else alphabet
            #assert set(have.keys()) == set(alphabet), \
            #    'Keys differ.\n  have keys  = %s\n  want keys = %s' % (set(have.keys()), set(alphabet))
            want = [want.get(k, 0) for k in alphabet]
            have = [have.get(k, 0) for k in alphabet]

        if isinstance(want, np.ndarray) and isinstance(have, np.ndarray):
            assert alphabet is None
            alphabet = Alphabet(dict(np.ndenumerate(want)).keys())

            assert want.shape == have.shape, [want.shape, have.shape]
            want = want.flatten()
            have = have.flatten()

        if data is not None:
#            assert isinstance(want, (int, str)), \
#                'expected a column name have %s' % type(want)
#            assert isinstance(have, (int, str)), \
#                'expected a column name have %s' % type(have)

            if want_label is None: want_label = want
            if have_label is None: have_label = have

            want = data[want]
            have = data[have]

        else:
            if want_label is None: want_label = 'want'
            if have_label is None: have_label = 'have'

            want = np.asarray(want)
            have = np.asarray(have)

            data = pd.DataFrame({want_label: want, have_label: have})

        assert want.shape == have.shape, [want.shape, have.shape]
        [n] = want.shape

        self.want = want
        self.have = have
        self.alphabet = alphabet
        self.ax = ax
        self.have_label = have_label
        self.want_label = want_label
        self.n = n
        self.coeff = None

        self.tests = tests = []

        # Check that vectors are finite.
        if not np.isfinite(want).all():
            tests.append(['want finite', progress(np.isfinite(want).sum(), n), False])
        if not np.isfinite(have).all():
            tests.append(['have finite', progress(np.isfinite(have).sum(), n), False])

        ne = norm(want)
        ng = norm(have)
        ok = abs(ne-ng)/ne < 0.01 if ne != 0 else True

        if n > 1:
            tests.append(['norms', '[%g, %g]' % (ne, ng), ok])
            #F = zero_retrieval(want, have)
            #tests.append(['zero F1', F, F > 0.99])

        # Correlation statistics
        if n > 1:
            #self.cosine = cosine(want, have)
            #tests.append(['cosine', self.cosine, (self.cosine > 0.99999)])   # cosine similarities must be really high.
            self.pearson = 1.0 if ne == ng == 0 else pearsonr(want, have)[0]
            tests.append(['pearson', self.pearson, (self.pearson > 0.99999)])
            self.spearman = spearmanr(want, have)[0]
            tests.append(['spearman', self.spearman, (self.spearman > 0.99999)])

        # TODO: this check should probably take into account the scale of the data.
        d = linf(want, have)
        self.max_err = d
        tests.append(['ℓ∞', d, None])
        tests.append(['ℓ₂', np.linalg.norm(want - have), None])

        # same sign check (weak agreement, but useful sanity check -- especially
        # for gradients)
        x = want
        y = have
        s = np.asarray(~((x >= 0) ^ (y >= 0)), dtype=int)
        p = s.sum() * 100.0 / len(s)
        tests.append(['same-sign', f'{p:.2f}% ({s.sum()}/{len(s)})', p == 100.0])

        # relative error
        r = relative_difference(want, have)
        r = np.max(r[np.isfinite(r)])
        #tests.append(['max rel err', r, r <= 0.01])
        self.max_relative_error = r
        self.max_rel_err = r

        # TODO: suggest that if relative error is high and rescaled error is low (or
        # something to do wtih regression residuals) that maybe there is a
        # (hopefully) simple fix via scale/offset.

        # TODO: can provide descriptive statistics for each vector
        #tests.append(['range (want)', [want.min(), want.max()], 2])
        #tests.append(['range (have)   ', [have.min(), have.max()], 2])

        # regression and rescaled error only valid for n >= 2
#        if n >= 2:
#            es = abs(want).max()
#            gs = abs(have).max()
#            if es == 0:
#                es = 1
#            if gs == 0:
#                gs = 1
#            if 0:
#                # rescaled error
#                E = want / es
#                G = have / gs
#                R = abs(E - G)
#                r = np.mean(R)
#                tests.append(['mean rescaled error', r, r <= 1e-5])

        if regression:
            self.regression()

        if n >= 2:
            # These tests check if one of the datasets is consistently larger than the
            # other. The threshold for error is based on `P_LARGER` ("percent larger").
            L = ((want-have) > 0).sum()
            if L >= P_LARGER * n:
                tests.append(['want is larger', progress(L, n), 0])
            L = ((have-want) > 0).sum()
            if L >= P_LARGER * n:
                tests.append(['have is larger', progress(L, n), 0])

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

#        if seaborn:
#            import seaborn as sns
#            sns.set_context(rc={"figure.figsize": (7, 5)})
#            g = sns.JointGrid(self.have_label, self.want_label, data=self.data)
#            g.plot(sns.regplot, sns.distplot, spearmanr)
#            print("Pearson's r: {0}".format(self.pearson))
#        else:
        if 1:
            if self.ax is None:
                self.ax = pl.figure().add_subplot(111)

            self.ax.scatter(self.have, self.want, lw=0, alpha=0.5, **scatter_kw)

            self.ax.set_xlabel(self.have_label)
            self.ax.set_ylabel(self.want_label)

            # Keeps the plot region tight against the data (allow 5% of the
            # data-range for padding so that points in the scatter plot aren't
            # partially clipped.)
#            xeps = 0.05 * np.ptp(self.have)
#            self.ax.set_xlim(self.have.min() - xeps, self.have.max() + xeps)

#            yeps = 0.05 * np.ptp(self.want)
#            self.ax.set_ylim(self.want.min() - yeps, self.want.max() + yeps)

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
            A[:,0] = self.have
            # plot estimated line
            ys = A @ self.coeff
            self.ax.plot(A[:,0], ys, c='r', alpha=0.5)
            self.ax.grid(True)
            self.ax.set_xlim(xa,xb)
        return self

    def regression(self):
        "least squares linear regression"
        if self.n < 2:
            return
        # data can't contain any NaNs
        if not np.isfinite(self.have).all() or not np.isfinite(self.want).all():
            self.tests.append(['regression',
                               'did not run due to NaNs in data',
                               0])
            return

        A = np.ones((self.n, 2))
        A[:,0] = self.have

        [self.coeff, residues, _, _] = lstsq(A, self.want)
        self.R = float(np.sqrt(residues)) if residues else 0.0

        # Label with warn or ok.
        ok = 1 if abs(self.coeff - [1, 0]).max() <= 1e-5 else 2

        slope = float(self.coeff[0])
        intercept = float(self.coeff[1])
        self.tests.append([
            'regression',
            f'[{slope:.3f} {intercept:.3f}] R={self.R:.3f}',
            ok
        ])

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

        s_want = dot_aligned(self.want)
        s_have = dot_aligned(self.have)

        if self.alphabet is None:
            self.alphabet = range(self.n)

        for (i,(x,y,sx,sy)) in enumerate(zip(self.want, self.have, s_want, s_have)):
            # XXX: skip zeros.
            #if abs(x) < 1e-10 and abs(y) < 1e-10:
            #    e = 0.0

            e = relative_difference(x, y)

            if e <= 0.001:
                continue

            df.append([e, self.alphabet.lookup(i), x, y, sx, sy])

            #df.append({'name':   alphabet[i],
            #           'error':  e,
            #           'want': x,
            #           'have':    y})

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
