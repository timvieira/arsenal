from numpy import array, log, dot, abs as np_abs

from scipy.maxentropy import logsumexp


log_of_2 = log(2)

def entropy(p):
    "Entropy of a discrete random variable with distribution `p`"
    assert len(p.shape) == 1
    p = p[p.nonzero()]
    return -dot(p, log(p)) / log_of_2

def kl_divergence(p, q):
    """ Compute KL divergence of two vectors, K(p || q).
    NOTE: If any value in q is 0.0 then the KL-divergence is infinite.
    """
    assert len(p) == len(q)
    p = p[p > 0]
    return dot(p, log(p / q)) / log_of_2

# KL(p||q) = sum_i p[i] log(p[i] / q[i])
#          = sum_i p[i] (log p[i] - log q[i])
#          = sum_i p[i] log p[i] - sum_i p[i] log(q[i])
#          = H(p) + CE(p,q)

def cross_entropy(p, q):
    """ Cross Entropy of two vectors, 

    CE(p,q) = - \sum_i p[i] log q[i]

    Relationship to KL-divergence:

      CE(p,q) = entropy(p) + KL(p||q)
    """
    assert len(p) == len(q)
    p = p[p > 0]
    return -dot(p, log(q)) / log_of_2

def assert_isdistr(p):
    assert (p >= 0).all()
    assert (p <= 1).all()
    assert abs(p.sum() - 1.0) < 0.000001

def normalize(p):
    return (1.0 / p.sum()) * p

# Lidstone smoothing is a generalization of Laplace smoothing.
def lidstone(p, delta):
    return normalize(p + delta)

def equal(a, b, epsilon=1e-10):
    "L_{\inf}(a - b) < epsilon"
    return np_abs(a - b).max() < epsilon

if __name__ == '__main__':
    import doctest; doctest.testmod()

    def tests():
        # Entropy tests
        assert entropy(array((0.5, 0.5))) == 1.0
        assert abs(entropy(array((0.75, 0.25))) - 0.8112781244) < 1e-10
        assert abs(entropy(array((0.1, 0.1, 0.8))) - 0.9219280948) < 1e-10
    
        # KL-divergence tests
        assert kl_divergence(array((0.5, 0.5)), array((0.5, 0.5))) == 0.0

        # KL, Entropy, and Cross Entropy relationship
        p = array([0.5, 0.5])
        q = array([0.4, 0.6])
        print equal(cross_entropy(p, q), (entropy(p) + kl_divergence(p, q)))

        # Normalize tests
        assert equal(array([0.5, 0.5]), normalize(array([2, 2])))

    tests()
