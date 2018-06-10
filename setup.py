#from distutils.core import setup, find_packages
from setuptools import setup, find_packages

setup(name='arsenal',
      version='3.0',
      description='Arsenal of python utilities.',
      author='Tim Vieira',
      url='https://github.com/timvieira/arsenal/',
      install_requires=[
#          'keyring',        # this is an annoying dependency
          'numpy',
          'colored',
          'path.py',
      ],
      packages=find_packages())
