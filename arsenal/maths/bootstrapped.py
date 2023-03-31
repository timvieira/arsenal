import numpy as np, pylab as pl
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def bootstrapped_model(xs, ys, degree, n_bootstraps=3000):
    #xs = np.linspace(0,1,100)
    #ys = xs**2 + np.random.normal(0,.05,size=100)


    pl.scatter(xs, ys, color='blue', marker='.', s=1, label='Data')

    #xs = np.array(xs); ys = np.array(ys)
    #xs = xs[np.isfinite(ys)]; ys = ys[np.isfinite(ys)]
    #xs = xs[np.argsort(xs)]; ys = ys[np.argsort(xs)]

    x = np.atleast_2d(xs).T
    y = np.array(ys)



    xdomain = np.linspace(xs.min(), xs.max(), 1000)

    predictions = np.zeros((n_bootstraps, len(xdomain)))

    for i in range(n_bootstraps):

        indices = np.random.choice(len(x), len(x), replace=True)

        model = LinearRegression()
        poly = PolynomialFeatures(degree=degree, include_bias=True)
        poly_features = poly.fit_transform(x[indices])

        model.fit(poly_features, y[indices])

        predictions[i, :] = model.predict(poly.fit_transform(np.atleast_2d(xdomain).T))  # Save the predictions for each bootstrap sample

    alpha = 0.05  # Set the significance level
    lower_ci = np.percentile(predictions, 100 * alpha / 2, axis=0)
    upper_ci = np.percentile(predictions, 100 * (1 - alpha / 2), axis=0)

    mean_pred = np.mean(predictions, axis=0)

    pl.ylim(y.min(), y.max())

    pl.plot(xdomain, mean_pred, color='k', label='mean')
    pl.fill_between(xdomain, lower_ci, upper_ci, color='gray', alpha=0.2,
                    label='95% predictive interval')
    pl.legend(loc='best')


def test_basics():

    n = 1000
    xs = np.random.uniform(-5, 5, size=n)
    ys = xs * np.cos(xs*5) + np.random.normal(0,.5,size=n)

    bootstrapped_model(xs, ys, degree=20)
    pl.show()




if __name__ == '__main__':
    from arsenal import testing_framework
    testing_framework(globals())
