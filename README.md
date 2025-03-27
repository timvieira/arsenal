# Arsenal

The arsenal is an assortment of python utilities that I can't live without.

## Documentation

[Read the Docs](https://python-arsenal.readthedocs.io/en/latest/)

## Setup

Optional: Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

To install the latest release:

```bash
pip install arsenal
```
    
To install the latest version from GitHub:

```bash
pip install git+https://github.com/timvieira/arsenal.git
```

Alternatively,

```bash
git clone https://github.com/timvieira/arsenal.git
cd arsenal
pip install -e .
```

## Running Tests

To run the test suite:

```bash
python -m unittest discover arsenal/tests
```

You can also run specific test files:

```bash
python -m unittest arsenal/tests/test_specific.py
```
