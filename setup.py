#from distutils.core import setup, find_packages
from setuptools import setup, find_packages

setup(name='arsenal',
      version='1.01',
      description='Arsenal of python utilities.',
      author='Tim Vieira',
      url='https://github.com/timvieira/arsenal/',
      install_requires=[
          'keyring',
          'numpy',
          'colored',
          'path.py',
      ],
      packages=find_packages())
