# Contributing to Django BigQuery Connector

Thank you for considering contributing to the Django BigQuery Connector! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository on GitHub.

2. Clone your fork locally:
   ```bash
   git clone https://github.com/ossown/django-bigquery-connector.git
   cd django-bigquery-connector
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Running Tests

Use pytest to run the test suite:

```bash
pytest
```

## Development Workflow

1. Create a branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and write tests if applicable.

3. Run the tests to ensure they pass:
   ```bash
   pytest
   ```

4. Format your code according to the project's style guidelines.

5. Commit your changes with a descriptive message.

6. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Open a pull request on GitHub.

## Pull Request Guidelines

- Include a clear description of the changes.
- Include test cases for new features or bug fixes.
- Ensure all tests pass.
- Reference any related issues.

## Code Style

- Follow PEP 8 guidelines for Python code.
- Use clear, descriptive variable and function names.
- Add docstrings to functions and classes.

## Reporting Bugs

When reporting bugs, please include:

- A clear, descriptive title.
- Steps to reproduce the issue.
- Expected behavior and actual behavior.
- Version information (Django, Python, BigQuery library versions).

## Feature Requests

Feature requests are welcome. Please provide:

- A clear description of the feature.
- Any relevant context or use cases.
- If possible, an outline of how you envision the implementation.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.