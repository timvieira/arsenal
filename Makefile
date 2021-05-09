cython:
	python setup.py build_ext -i

doc:
	sphinx-apidoc -o docs arsenal --full
	(cd docs && make html)

clean:
	rm -rf coverage-report .coverage
	rm -rf docs/_build docs/_templates docs/_static

coverage:
	find arsenal -name '*.py' -exec coverage run --rcfile .coveragerc -a {} \;
	coverage html --rcfile .coveragerc --include './*' -d coverage-report
	xdg-open coverage-report/index.html

test:
	find arsenal -name '*.py' -exec python {} \;
