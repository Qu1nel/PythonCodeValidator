# Contributing to Python Code Validator

First and foremost, thank you for considering contributing to this project! We welcome any and all contributions, from
fixing a typo in the documentation to implementing a brand new validation rule.

This document provides guidelines to ensure that contributing is a smooth and effective process for everyone involved.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements or New Features](#suggesting-enhancements-or-new-features)
    - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Setup](#development-setup)
- [Styleguides](#styleguides)
    - [Git Commit Messages](#git-commit-messages)
    - [Python Styleguide](#python-styleguide)
- [Testing](#testing)

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](./CODE_OF_CONDUCT.md). Please read it
before you start.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please ensure it hasn't already been reported by searching through
the [GitHub Issues](https://github.com/Qu1nel/PythonCodeValidator/issues). If you're unable to find an open issue
addressing the problem,
please [open a new one](https://github.com/Qu1nel/PythonCodeValidator/issues/new?template=1-bug-report.md) using the "
Bug Report" template.

### Suggesting Enhancements or New Features

We are always open to new ideas! If you have a suggestion for an enhancement to an existing feature or a new feature
entirely, please open an issue using the appropriate template:

- [**Feature Request**](https://github.com/Qu1nel/PythonCodeValidator/issues/new?template=4-feature-request.md) for new
  ideas.
- [**Enhancement Request**](https://github.com/Qu1nel/PythonCodeValidator/issues/new?template=5-enhancement-request.md)
  for improving existing functionality.

### Submitting Pull Requests

If you have code to contribute, please submit it as a Pull Request (PR).

1. Fork the repository and create your branch from `main`.
2. Set up your local development environment (see [Development Setup](#development-setup)).
3. Make your changes.
4. Ensure your code lints and passes all tests (see [Styleguides](#styleguides) and [Testing](#testing)).
5. Update the `README.md` and any other relevant documentation if your changes require it.
6. Open a new Pull Request, filling out the provided template.

## Development Setup

We use `uv` for package and environment management. The easiest way to get started is with `make`.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Qu1nel/PythonCodeValidator.git
   cd PythonCodeValidator
   ```
2. **Run the setup command:**
   ```bash
   make setup
   ```
   This command will create a virtual environment in `.venv/` and install all necessary dependencies for development.

3. **Activate the virtual environment:**
    * On Linux/macOS: `source .venv/bin/activate`
    * On Windows: `.venv\Scripts\activate`

Now you are ready to start coding!

## Styleguides

### Git Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This helps us
automate versioning and changelogs. Please structure your commit messages accordingly.

Examples:

- `feat: Add new 'must_be_constant' constraint`
- `fix: Correctly handle relative imports in ImportStatementSelector`
- `docs: Update README with new installation instructions`
- `test: Add unit tests for scope_handler`
- `refactor: Improve performance of AST traversal`
- `chore: Update CI workflow to use Python 3.12`

### Python Styleguide

Our codebase is automatically formatted and linted using **Ruff**. Before committing, please run:

```bash
make lint
```

This command will format your code and check for any style violations, attempting to fix them automatically.

## Testing

This project maintains a high standard of test coverage.

- **Run the full test suite:**
  ```bash
  make test
  ```
- **Run tests with a coverage report:**
  ```bash
  make coverage
  ```
- **Generate an interactive HTML coverage report:**
  ```bash
  make coverage-html
  ```
  This will create a report in the `htmlcov/` directory.

All new features and bug fixes **must** be accompanied by corresponding tests to be accepted.

---

Thank you again for your interest in contributing!