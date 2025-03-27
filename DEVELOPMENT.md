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

Update: Building and publishing are handled by Github actions.

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

