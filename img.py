from numpy.lib import gradient
from numpy.core import uint32, float32
from numpy.core import abs

def rgb_to_grayscale(img):
    """
    Return a NxM matrix in grayscale from a NxMx3 matrix in RGB.
    """
    return (img[:,:,0].astype(uint32) * 30 + \
            img[:,:,1].astype(uint32) * 59 + \
            img[:,:,2].astype(uint32) * 11) / 100

def energy(img):
    """
    Return a NxM matrix of the gradients from a NxMx3 matrix.
    """
    [gradx, grady] = gradient(img.astype(float32))
    return abs(gradx) + abs(grady)
