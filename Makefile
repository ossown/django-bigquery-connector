.PHONY: clean clean-test clean-pyc clean-build docs help test test-local
.DEFAULT_GOAL := help

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "test-local - run tests locally with proper PYTHONPATH"
	@echo "dist - build package for distribution"
	@echo "release - package and upload a release"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

test:
	pytest

test-local:
	PYTHONPATH=$$PYTHONPATH:. pytest

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

release: dist
	twine upload dist/*

install: clean
	pip install .