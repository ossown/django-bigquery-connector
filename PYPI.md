# Publishing to PyPI

This document outlines the steps to publish the django-bigquery-connector package to PyPI.

## Prerequisites

Ensure you have the following tools installed:

```bash
pip install wheel twine
```

## Building the Package

1. Make sure all files are properly structured in the package directory.

2. Update version number in:
   - `setup.py`
   - `django_bigquery_connector/__init__.py`

3. Build the package:

```bash
python setup.py sdist bdist_wheel
```

4. Check the built packages:

```bash
ls -l dist/
```

## Testing the Package Locally

Before uploading to PyPI, you can test your package locally:

```bash
pip install -e .
```

Or install the built wheel directly:

```bash
pip install dist/django_bigquery_connector-0.1.0-py3-none-any.whl
```

## Uploading to TestPyPI

It's recommended to test your package on TestPyPI first:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Then install from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ django-bigquery-connector
```

## Uploading to PyPI

Once you've verified the package works correctly:

```bash
twine upload dist/*
```

## Installation from PyPI

After publishing, users can install your package with:

```bash
pip install django-bigquery-connector
```

## Important Notes

- Before publishing a new version, delete the old build files in the `dist/` directory
- Make sure all dependencies are correctly specified in `setup.py`
- Ensure your README.md is accurate and provides clear installation/usage instructions
- Remember to update the version number before each new release