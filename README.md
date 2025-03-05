# Arsenal

The arsenal is an assortment of python utilities that I can't live without.

## Setup

1. Create and activate a virtual environment:

```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the package and development dependencies:

```bash
    git clone https://github.com/timvieira/arsenal.git
    cd arsenal
    pip install -e .
```

Alternatively, use pip to install from GitHub:

```bash
    pip install git+https://github.com/timvieira/arsenal.git
```

## Development Tasks

The Makefile provides several useful commands:

```bash
    make cython      # Build Cython extensions
    make doc         # Generate documentation using Sphinx
    make test        # Run all tests
    make coverage    # Generate test coverage report
    make clean       # Clean build artifacts and documentation
```

## Building and Publishing

1. Install build tools:
    
```bash
    pip install build twine
```

2. Clean old distributions:

```bash
    rm -rf dist/ build/ *.egg-info
```

3. Create distribution packages:

```bash
    make cython
    python -m build
```

4. Check the distributions:

```bash
    twine check dist/*
```

5. Upload to Test PyPI first:

```bash
    twine upload --repository testpypi dist/*
```

6. If everything looks good, upload to PyPI:

```bash
    twine upload dist/*
```

Note: You'll need a PyPI account and API token. Store your credentials in `~/.pypirc` or enter them when prompted.

## Documentation

[Read the Docs](https://python-arsenal.readthedocs.io/en/latest/)

## Running Tests

To run the test suite:

```bash
    python -m unittest discover arsenal/tests
```

You can also run specific test files:

```bash
    python -m unittest arsenal/tests/test_specific.py
```
