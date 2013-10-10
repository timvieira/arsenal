import numpy
import scipy
import scipy.linalg

try:
    from arsenal.iterextras import iterview
except ImportError:
    iterview = lambda x, *args, **kw: x

def ransac(data, model, n, k, t, d, debug=False):
    """
    fit model parameters to data using the RANSAC algorithm

    This implementation written from pseudocode found at
        http://en.wikipedia.org/w/index.php?title=RANSAC&oldid=116358182

    Given:
        data - a set of observed data points
        model - a model that can be fitted to data points
        n - the minimum number of data values required to fit the model
        k - the maximum number of iterations allowed in the algorithm
        t - a threshold value for determining when a data point fits a model
        d - the number of close data values required to assert that a model fits well to data
    Return:
        bestfit - model parameters which best fit the data (or None if no good model is found)
    """

    bestfit          = None
    besterr          = numpy.inf
    best_inlier_idxs = None

    for i in iterview(xrange(k), 250):
        # randomly partition data (random_partition returns two arrays of ids)
        maybe_idxs, test_idxs = random_partition(n, data.shape[0])

        # get data points for each id
        maybeinliers = data[maybe_idxs,:]
        test_points  = data[test_idxs]

        # fit model and check error on the test points
        maybemodel   = model.fit(maybeinliers)
        test_err     = model.get_error(test_points, maybemodel)

        # pick indices of test_points with acceptable error (below threshold)
        also_idxs    = test_idxs[test_err < t]
        alsoinliers  = data[also_idxs,:]

        if debug:
            print 'test_err.min()', test_err.min()
            print 'test_err.max()', test_err.max()
            print 'numpy.mean(test_err)', numpy.mean(test_err)
            print 'iteration %d: len(alsoinliers) = %d' % (i, len(alsoinliers))

        # Do we have enough values not included in the fit-partition to assert that
        # maybemodel fits well-enough?
        if len(alsoinliers) > d:

            betterdata  = numpy.concatenate((maybeinliers, alsoinliers))
            bettermodel = model.fit(betterdata)
            better_errs = model.get_error(betterdata, bettermodel)  # SSE per row
            thiserr     = numpy.mean(better_errs)

            # only keep the best model, error, and data
            if thiserr < besterr:
                bestfit = bettermodel
                besterr = thiserr
                best_inlier_idxs = numpy.concatenate((maybe_idxs, also_idxs))

    if bestfit is None:
        raise ValueError("did not meet fit acceptance criteria")

    return bestfit, {'inliers': best_inlier_idxs}

def random_partition(n, n_data):
    """return n random rows of data (and also the other len(data)-n rows)"""
    all_idxs = numpy.arange(n_data)
    numpy.random.shuffle(all_idxs)
    idxs1 = all_idxs[:n]
    idxs2 = all_idxs[n:]
    return idxs1, idxs2

# TODO: model and params seems to be used interchangeably in some parts..
class LinearLeastSquaresModel(object):
    """
    linear system solved using linear least squares

    This class serves as an example that fulfills the model interface
    needed by the ransac() function.
    """
    def __init__(self, input_columns, output_columns, debug=False):
        self.input_columns = input_columns
        self.output_columns = output_columns
        self.debug = debug
    def fit(self, data):
        A = numpy.vstack([data[:,i] for i in self.input_columns]).T
        B = numpy.vstack([data[:,i] for i in self.output_columns]).T
        x, resids, rank, s = scipy.linalg.lstsq(A, B)
        return x
    def get_error(self, data, model):
        A = numpy.vstack([data[:,i] for i in self.input_columns]).T
        B = numpy.vstack([data[:,i] for i in self.output_columns]).T
        B_fit = scipy.dot(A, model)
        err_per_point = numpy.sum((B-B_fit)**2, axis=1) # sum squared error per row
        return err_per_point


from sklearn.linear_model import Ridge

class RidgeRegressionModel(LinearLeastSquaresModel):
    def __init__(self, input_columns, output_columns, debug=False):

        self.alpha = 0.0000000001
        self.m = Ridge(alpha=self.alpha)

        super(RidgeRegressionModel, self).__init__(input_columns, output_columns, debug=debug)

    def fit(self, data):
        A = numpy.vstack([data[:,i] for i in self.input_columns]).T
        B = numpy.vstack([data[:,i] for i in self.output_columns]).T

        self.m.fit(A, B)

        return self.m.coef_   #m.intercept_

    def get_error(self, data, model):
        A = numpy.vstack([data[:,i] for i in self.input_columns]).T
        B = numpy.vstack([data[:,i] for i in self.output_columns]).T
        B_fit = scipy.dot(A, model)
        err_per_point = numpy.sum((B-B_fit)**2, axis=1) # sum squared error per row

        norm = numpy.sqrt(model*model)
        assert norm.shape == (1,1)
        regularizer = 1.0*norm[0,0]

        return err_per_point - regularizer


class Perceptron(LinearLeastSquaresModel):
    def __init__(self, input_columns, output_columns, debug=False):
        LinearLeastSquaresModel.__init__(self, input_columns, output_columns, debug=debug)

    def fit(self, data):
        A = numpy.vstack([data[:,i] for i in self.input_columns]).T
        B = numpy.vstack([data[:,i] for i in self.output_columns]).T
        w = numpy.zeros((1, len(A[0]) + 1))
        for i in xrange(100):
            for x, y in zip(A,B):
                x = numpy.append(x, 1)
                z = numpy.dot(w, x)
                w += 0.000005*((y-z)*x - 100.0*w)
        return w


def test():
    # generate perfect input data
    n_samples = 300
    n_inputs  = 1
    n_outputs = 1
    A_exact     = 20*numpy.random.random((n_samples, n_inputs))
    perfect_fit = 60*numpy.random.normal(size=(n_inputs, n_outputs)) # the model
    B_exact     = scipy.dot(A_exact, perfect_fit)
    assert B_exact.shape == (n_samples, n_outputs)

    # add a little Gaussian noise (linear least squares alone should handle this well)
    A_noisy = A_exact + numpy.random.normal(size=A_exact.shape)
    B_noisy = B_exact + numpy.random.normal(size=B_exact.shape)

    # add some outliers, by perturbing a portion of the data
    if 1:
        n_outliers = 40
        outlier_idxs, non_outlier_idxs = random_partition(n_outliers, A_noisy.shape[0])
        A_noisy[outlier_idxs] = 20*numpy.random.random((n_outliers, n_inputs)) + 20
        B_noisy[outlier_idxs] = 50*numpy.random.normal(size=(n_outliers, n_outputs))

    # setup model
    all_data       = numpy.hstack((A_noisy, B_noisy))
    input_columns  = range(n_inputs)
    output_columns = [n_inputs+i for i in xrange(n_outputs)]
    debug = False

    least_squares = LinearLeastSquaresModel(input_columns, output_columns, debug=debug)
    perceptron = Perceptron(input_columns, output_columns, debug=debug)
    ridge_model = RidgeRegressionModel(input_columns, output_columns, debug=debug)

    #model = perceptron
    model = least_squares
    #model = ridge_model

    # run RANSAC algorithm
    ransac_fit, ransac_data = ransac(all_data, model, 30, 50, 1e3, 10, debug=debug)

    # what happens if we fit the model to all the data?
    linear_fit = least_squares.fit(all_data)
    ridge_fit = ridge_model.fit(all_data)
    perceptron_fit = perceptron.fit(all_data)

    # plotting
    import pylab
    sort_idxs = numpy.argsort(A_exact[:,0])
    A_col0_sorted = A_exact[sort_idxs]       # maintain as rank-2 array

    # color the outliers generated differently from all data?
    if 1:
        pylab.plot(A_noisy[non_outlier_idxs,0], B_noisy[non_outlier_idxs,0], 'k.', label='noisy data' )
        pylab.plot(A_noisy[outlier_idxs,0],     B_noisy[outlier_idxs,0],     'r.', label='outlier data' )
    else:
        pylab.plot(A_noisy[:,0], B_noisy[:,0], 'k.', label='data')

    # show data point used in RANSAC's fit
    if 1:
        pylab.plot(A_noisy[ransac_data['inliers'],0], B_noisy[ransac_data['inliers'],0], 'bx', label='RANSAC data')

    pylab.plot(A_col0_sorted[:,0], numpy.dot(A_col0_sorted, ransac_fit)[:,0],  label='RANSAC fit')
    pylab.plot(A_col0_sorted[:,0], numpy.dot(A_col0_sorted, perfect_fit)[:,0], label='exact system')
    pylab.plot(A_col0_sorted[:,0], numpy.dot(A_col0_sorted, linear_fit)[:,0],  label='linear fit')
    pylab.plot(A_col0_sorted[:,0], numpy.dot(A_col0_sorted, ridge_fit)[:,0],  label='ridge fit')
    pylab.plot(A_col0_sorted[:,0], numpy.dot(A_col0_sorted, perceptron_fit)[:,0],  label='perceptron fit')

    pylab.legend()

    #pylab.legend()
    pylab.show()


if __name__=='__main__':
    test()
