import numpy as np
import setuptools
from setuptools import setup, find_packages
from Cython.Build import cythonize


with open('README.md', "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='arsenal',
    version='3.0',
    author='Tim Vieira',
    author_email='tim.f.vieira@gmail.com',
    description = 'Arsenal of python utilities.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/timvieira/arsenal/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires = [
        #'keyring',        # this is an annoying dependency
        'numpy',
        'scipy',
        'pandas',
        'cython',
        'orderedset',
        'matplotlib',
        'gprof2dot',
        #'blist',
        #'colored',
        'path.py',
        #'blist',
    ],
    ext_modules = cythonize(['arsenal/**/*.pyx']),
    include_dirs = [np.get_include()],
)
