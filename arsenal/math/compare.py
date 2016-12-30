import numpy as np
import pylab as pl
import pandas as pd
from numpy import isfinite
from scipy.linalg import norm
from arsenal.iterview import progress
from scipy.stats import pearsonr, spearmanr
from arsenal.math.util import cosine, linf, relative_difference, zero_retrieval
from arsenal import colors
from scipy.linalg import lstsq


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

         - Allow user to specify alternative names to `expect` and `got` since they
           are often confusing.

         - Add an option to drop NaNs and continue comparison.

         - Support dictionarys as input with named dimensions and/or possibly an
           alphabet for naming dimensions.

         - Indicate which dimensions have the largest errors.

        """

        if isinstance(expect, dict) and isinstance(got, dict):
            _alphabet = expect.keys() if alphabet is None else alphabet
            assert set(got.keys()) == set(_alphabet)
            expect = [expect[k] for k in _alphabet]
            got = [got[k] for k in _alphabet]

        if data is not None:
            assert isinstance(expect, (int, basestring)), \
                'expected a column name got %s' % type(expect)
            assert isinstance(got, (int, basestring)), \
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

        assert expect.shape == got.shape
        [n] = expect.shape

        self.expect = expect
        self.got = got
        self.alphabet = alphabet
        self.ax = ax
        self.name = name
        self.got_label = got_label
        self.expect_label = expect_label
        self.n = n
        self.coeff = None

        self.tests = tests = []

        # Check that vectors are finite.
        if not isfinite(expect).all():
            tests.append(['expect finite', progress(isfinite(expect).sum(), n), False])
        if not isfinite(got).all():
            tests.append(['got finite', progress(isfinite(got).sum(), n), False])

        ne = norm(expect)
        ng = norm(got)
        ok = abs(ne-ng)/ne < 0.01 if ne != 0 else True

        if n > 1:
            tests.append(['norms', '[%g, %g]' % (ne, ng), ok])

            # TODO: what do we want to say about sparsity?
            #tests.append(['zeros', '%s %s' % (progress((expect==0).sum(), n),
            #                                  progress((got==0).sum(), n)),
            #              -1])
            F = zero_retrieval(expect, got)
            tests.append(['zero F1', F, F > 0.99])

        if n > 1:
            c = cosine(expect, got)
            self.cosine = c
            tests.append(['cosine-sim', c, (c > 0.99999)])   # cosine similarities must be really high.

            self.pearsonr = 1.0 if ne == ng == 0 else pearsonr(expect, got)[0]
            tests.append(['pearson', self.pearsonr, (self.pearsonr > 0.99999)])

            p = spearmanr(expect, got)[0]
            tests.append(['spearman', p, (p > 0.99999)])

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
        r = np.mean(r[isfinite(r)])
        tests.append(['mean relative error', r, r <= 0.01])

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

        if alphabet is not None:
            self.show_largest_rel_errors()

    def message(self):
        print
        print 'Comparison%s:' % (' (%s)' % self.name if self.name else ''), 'n=%s' % self.n
        #print yellow % 'expected:'
        #print expect
        #print yellow % 'got:'
        #print got
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
            print '  %s: %s' % (k, c % (v,))
        print

    def plot(self, regression=True, seaborn=False, ax=None, **scatter_kw):
        if ax is not None:
            self.ax = ax
        if seaborn:
            import seaborn as sns
            sns.set_context(rc={"figure.figsize": (7, 5)})
            g = sns.JointGrid(self.got_label, self.expect_label, data=self.data)
            g.plot(sns.regplot, sns.distplot, spearmanr)
            print "Pearson's r: {0}".format(self.pearsonr)
        else:
            if self.ax is None:
                self.ax = pl.figure().add_subplot(111)
            self.ax.scatter(self.got, self.expect, lw=0, alpha=0.5, **scatter_kw)
            if self.name is not None:
                self.ax.set_title(self.name)
            self.ax.set_xlabel(self.got_label)
            self.ax.set_ylabel(self.expect_label)
        if regression:
            self.regression_line()
        return self

    def show(self, *args, **kw):
        self.plot(*args, **kw)
        pl.show()
        return self

    def regression_line(self):
        # TODO: write the coeff to plot.
        if self.coeff is not None and isfinite(self.coeff).all():
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

        # TODO: for regression we want parameters `[1 0]` and a small
        # residual. We want both these conditions to hold. Might be
        # useful to look at R^2 statistic since it normalizes scale and
        # number of data-points. (it's often used for reduction in
        # variance.)

        # data can't contain any NaNs
        if not isfinite(self.got).all() or not isfinite(self.expect).all():
            self.tests.append(['regression',
                               'did not run due to NaNs in data',
                               0])
            return

        if self.n < 2:
#            self.tests.append(['regression',
#                               'too few points',
#                               0])
            return

        A = np.ones((self.n, 2))
        A[:,0] = self.got

        self.coeff, _, _, _ = lstsq(A, self.expect)

        # Label with warn or ok.
        ok = 1 if abs(self.coeff - [1, 0]).max() <= 1e-5 else 2

        self.tests.append(['regression', '[%.3f %.3f]' % (self.coeff[0], self.coeff[1]), ok])

    def show_largest_rel_errors(self):
        "show largest relative errors"

        df = []

        #es = abs(expect).max()
        #gs = abs(got).max()

        for (i,(x,y)) in enumerate(zip(self.expect, self.got)):
            # XXX: skip zeros.
            #if abs(x) < 1e-10 and abs(y) < 1e-10:
            #    e = 0.0

            e = relative_difference(x, y)

            if e <= 0.001:
                continue

            df.append([e, self.alphabet[i], x, y])

            #df.append({'name':   alphabet[i],
            #           'error':  e,
            #           'expect': x,
            #           'got':    y})

        df.sort(reverse=1)

        if len(df):
            print ' Relative errors'
            print ' ==============='
            for e, n, x, y in df:

                types = []
                if x < y:
                    types.append('bigger')
                else:
                    types.append('smaller')

                # highlight sign errors.
                #if np.sign(x) != np.sign(y):
                if (x >= 0) != (y >= 0):
                    types.append(colors.red % 'wrong sign')

                print '  %-15s %.5f %g %g' % (n, e, x, y), \
                    ((colors.green % 'ok') if e <= 0.01 else colors.red % 'bad'), \
                    '(%s)' % (', '.join(types))

        #from pandas import DataFrame
        #df = DataFrame(df)
        #df.set_index('name', inplace=1)
        #print df.sort('error', ascending=0)


if __name__ == '__main__':

    def test_compare():
        n = 100
        # `a` is a noisy version of `b`, but tends to overestimate.
        a = np.linspace(0,1,n)
        b = a + np.random.uniform(-0.01, 0.1, size=n)
        compare(a,b).show()
        compare('a', 'b', data=pd.DataFrame({'a': a, 'b': b})).show()

    test_compare()
