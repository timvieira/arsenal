cython:
	pip install -e .

test:
	python -m pytest tests/

doc:
	sphinx-apidoc -o docs arsenal --full
	(cd docs && make html)

coverage:
	python -m pytest tests/ --cov=arsenal --cov-report=html:coverage-report
	xdg-open coverage-report/index.html

clean:
	rm -rf coverage-report .coverage
	rm -rf docs/_build docs/_templates docs/_static
	rm -rf build dist *.egg-info
