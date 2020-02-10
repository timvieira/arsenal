#from distutils.core import setup, find_packages
import numpy as np
from setuptools import setup, find_packages
from Cython.Build import cythonize


setup(name = 'arsenal',
      version = '3.2',
      description = 'Arsenal of python utilities.',
      author = 'Tim Vieira',
      url = 'https://github.com/timvieira/arsenal/',
      install_requires = [
          #'keyring',        # this is an annoying dependency
          'numpy',
          'colored',
          'path.py',
          'blist',
      ],
      packages = find_packages(),
      ext_modules = cythonize(['arsenal/**/*.pyx']),
      include_dirs = [np.get_include()],
)
