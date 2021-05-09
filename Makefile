cython:
	python setup.py build_ext -i

docs:
	sphinx-apidoc -o docs arsenal --full
	(cd docs && make html)

clean:
	rm -rf coverage-report .coverage
	rm -rf docs

coverage:
	find arsenal -name '*.py' -exec coverage run --rcfile .coveragerc -a {} \;
	coverage html --rcfile .coveragerc --include './*' -d coverage-report
	xdg-open coverage-report/index.html
