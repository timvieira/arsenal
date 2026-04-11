import numpy as np, pylab as pl

def bootstrapped_model(xs, ys, degree, n_bootstraps=3000):

    pl.scatter(xs, ys, color='blue', marker='.', s=1, label='Data')

    xs = np.asarray(xs)
    ys = np.asarray(ys)

    xdomain = np.linspace(xs.min(), xs.max(), 1000)

    predictions = np.zeros((n_bootstraps, len(xdomain)))

    for i in range(n_bootstraps):
        indices = np.random.choice(len(xs), len(xs), replace=True)
        coeffs = np.polyfit(xs[indices], ys[indices], degree)
        predictions[i, :] = np.polyval(coeffs, xdomain)

    alpha = 0.05
    lower_ci = np.percentile(predictions, 100 * alpha / 2, axis=0)
    upper_ci = np.percentile(predictions, 100 * (1 - alpha / 2), axis=0)

    mean_pred = np.mean(predictions, axis=0)

    pl.ylim(ys.min(), ys.max())

    pl.plot(xdomain, mean_pred, color='k', label='mean')
    pl.fill_between(xdomain, lower_ci, upper_ci, color='gray', alpha=0.2,
                    label='95% predictive interval')
    pl.legend(loc='best')

