#from distutils.core import setup, find_packages
from setuptools import setup, find_packages

setup(name='arsenal',
      version='1.01',
      description='Utils.',
      author='Tim Vieira',
      url='https://github.com/timvieira/arsenal/',
      packages= find_packages(),
      install_requires=['numpy'])
