# Contributing to Python Code Validator

First off, thank you for considering contributing! This project is a community effort, and we welcome any contribution,
from fixing a typo to implementing a new feature.

## Where to start?

- **Bug Reports:** If you found a bug, please check if it has already been reported in
  the [Issues](https://github.com/Qu1nel/PythonCodeValidator/issues). If not, please submit a new one using our "Bug
  Report" template.
- **Feature Requests:** Have an idea for a new feature or an enhancement? We'd love to hear it! Please use the "Feature
  Request" or "Enhancement Request" templates in the [Issues](https://github.com/Qu1nel/PythonCodeValidator/issues).
- **Questions:** If you have questions about how to use the validator or how it works, feel free to ask using the "
  Question or Support Request" template.

## Development Workflow

To contribute code, please follow these steps:

1. **Fork the repository** and clone it to your local machine.
2. **Set up the development environment.** We use `uv` for dependency management. From the project root, run:
   ```bash
   make setup
   ```
   This will create a virtual environment in `.venv/` and install all necessary dependencies.
3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate  # On Linux/macOS/WSL
   # or
   .venv\Scripts\activate    # On Windows
   ```
4. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/some-bug-fix
   ```
5. **Make your changes.** As you code, please ensure you follow our coding standards by running:
   ```bash
   make lint
   ```
6. **Add or update tests.** All new features must be accompanied by tests. All bug fixes must include a test that
   reproduces the bug. Run the full test suite with:
   ```bash
   make test
   ```
7. **Ensure high test coverage.** Check the coverage report:
   ```bash
   make coverage-html
   ```
8. **Update documentation.** If you added or changed a feature, please update the relevant documentation and docstrings.
9. **Commit your changes.** We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.
   This helps in automating changelogs and versioning.
    * `feat:` for a new feature.
    * `fix:` for a bug fix.
    * `docs:` for documentation changes.
    * `style:` for formatting changes.
    * `refactor:` for code changes that neither fix a bug nor add a feature.
    * `test:` for adding or refactoring tests.
    * `chore:` for build process or auxiliary tool changes.
10. **Push your branch and open a Pull Request.** Fill out the pull request template to help us understand and review
    your contribution.

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](./CODE_OF_CONDUCT.md).

Thank you for your contribution!