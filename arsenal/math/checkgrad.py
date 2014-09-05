import numpy as np
from numpy import zeros_like
from numpy.linalg import norm
from arsenal.iterview import iterview
from arsenal.terminal import green, red, yellow
from random import sample


# TODO: implement sign check (these are pretty bad errors), difference in scale
# TODO: unify with `arsenal.math.numpy_extras.compare`
def check_gradient(f, grad, theta, alphabet=None, eps=1e-4, tol=0.01, skip_zero=True,
                    verbose=True, random_subset=None):

    """Check gradient that `f(theta) == grad` by centered-difference approximation.

    Provides feedback on which dimensions differ

    Arguments:

     - `f`: function we are taking the gradient of.

     - `grad`: What we think the gradient is at `theta`.

     - `theta`:

     - `alphabet` (optional): a bijective map from strings to integers. Expects
       `arsenal.alphabet.Alphabet` instance. This is used to map integer-valued
       dimensions to human-readable names (e.g., strings).

     - `eps`: perturbation size

     - `tol`: what is deem an error (we use relative error)

     - `skip_zero`: good relative error is hard to get for values which are
       really small (near zero).

     - `random_subset`: number dimensions to probe in comparison (useful for
       high dimensions because this test is linear in the dimensionality of
       `theta`).

    """

    fails = 0

    grad = np.asarray(grad)

    if alphabet is not None:
        keys = alphabet._flip.keys()
        assert len(alphabet), 'Alphabet is empty.'
    else:
        keys = range(len(theta))

    if random_subset is not None:
        keys = sample(keys, min(len(keys), random_subset))

    assert len(keys) > 0

    fd = zeros_like(theta)
    for i in (iterview(keys, msg='checkgrad') if verbose else keys):
        was = theta[i]
        # perturb right
        theta[i] = was + eps
        right = f(theta)
        # perturb left
        theta[i] = was - eps
        left = f(theta)
        # reset
        theta[i] = was
        # centered difference
        fd[i] = (right - left) / (2*eps)

    w = max(map(len, alphabet.keys())) if alphabet is not None else 0

    nzeros = 0

    for i in keys:
        # check relative error

        if skip_zero and abs(fd[i]) < 1e-10 and abs(grad[i]) < 1e-10:  # both approximately zero
            nzeros += 1
            continue

        relative_error = abs(fd[i] - grad[i]) / max(abs(fd[i]), abs(grad[i]))
        if relative_error > tol:
            name = alphabet.lookup(i) if alphabet is not None else i
            fails += 1

            if verbose:
                print red % 'dim = %s rel-err = %5.3f' % (('%%-%ss' % w) % (name,), relative_error), \
                    'want: %g; got: %g' % (fd[i], grad[i])
            else:
                assert False, \
                    'dim = %s rel-err = %5.3f, want: %g; got: %g' \
                    % (('%%-%ss' % w) % (name,), relative_error, fd[i], grad[i])

    if nzeros * 1.0 / len(keys) >= 0.75:
        print yellow % '[warning] checkgradient skipped a lot of approximately zero components ' \
            'percentage= %g (%s/%s)' % (nzeros * 1.0 / len(keys), nzeros, len(keys))

    if verbose:
        print 'gradient:',
        if not fails:
            print green % 'OK',
        else:
            print red % 'failed %s of %s' % (fails, len(keys)),

        print 'cosine similarity: %g' % (np.dot(grad[keys], fd[keys]) / norm(grad[keys]) / norm(fd[keys]))

        # TODO: add sign check.

        #print norm(grad[keys]) / norm(fd[keys]), norm(fd[keys]) / norm(grad[keys])

        #print grad.dot(fd), norm(grad), norm(fd)
        #print 'factor:', fd.mean() / grad.mean()  # print scaling factor
