from distutils.core import setup

setup(name='arsenal',
      version='1.0',
      description='Utils.',
      author='Tim Vieira',
      url='https://github.com/timvieira/arsenal/',
      packages=['arsenal'],
      install_requires=['whoosh', 'pdfminer', 'pandas', 'numpy'])
