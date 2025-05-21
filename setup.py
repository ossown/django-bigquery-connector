from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

# Read the version from __init__.py
with open(os.path.join("django_bq", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        version = "0.1.0"

setup(
    name="django-bigquery-connector",
    version=version,
    author="Sidhavratha Kumar",
    author_email="your.email@example.com",
    description="Django ORM connector for Google BigQuery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ossown/django-bigquery-connector",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=[
        "django>=4.1",
        "google-cloud-bigquery>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-django>=4.0.0",
            "black",
            "flake8",
            "isort",
            "wheel",
            "twine",
        ],
    },
    keywords=["django", "bigquery", "database", "orm", "connector"],
    project_urls={
        "Bug Tracker": "https://github.com/ossown/django-bigquery-connector/issues",
        "Documentation": "https://github.com/ossown/django-bigquery-connector",
        "Source Code": "https://github.com/ossown/django-bigquery-connector",
    },
)