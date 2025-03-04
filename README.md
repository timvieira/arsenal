# Arsenal

The arsenal is an assortment of python utilities that I can't live without.

## Setup

1. Create and activate a virtual environment:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install the package and development dependencies:

    pip install -e .
    pip install build  # Required for building distributions

## Development Tasks

The Makefile provides several useful commands:

    make cython      # Build Cython extensions
    make doc         # Generate documentation using Sphinx
    make test        # Run all tests
    make coverage    # Generate test coverage report
    make clean       # Clean build artifacts and documentation

## Building and Publishing

1. Install build tools:

    pip install build twine

2. Clean old distributions:

    rm -rf dist/ build/ *.egg-info

3. Create distribution packages:

    python -m build

4. Check the distributions:

    twine check dist/*

5. Upload to Test PyPI first:

    twine upload --repository testpypi dist/*

6. Test the installation from Test PyPI:

    pip install --index-url https://test.pypi.org/simple/ arsenal

7. If everything looks good, upload to PyPI:

    twine upload dist/*

Note: You'll need a PyPI account and API token. Store your credentials in `~/.pypirc` or enter them when prompted.

## Documentation

[Read the Docs](https://python-arsenal.readthedocs.io/en/latest/)

## Alternative Installation Methods

If you prefer not to use a virtualenv, you can install directly:

1. Clone and pip-install:

    git clone https://github.com/timvieira/arsenal.git
    cd arsenal 
    pip install .

2. Use pip for the whole thing:

    pip install -r https://raw.githubusercontent.com/timvieira/arsenal/master/requirements.txt
    pip install git+https://github.com/timvieira/arsenal.git

Note: Just running the second command fails to identify the requirements file.

## Running Tests

To run the test suite:

    python -m unittest discover arsenal/tests

You can also run specific test files:

    python -m unittest arsenal/tests/test_specific.py
