************
Contributing
************

First and foremost, thank you for considering contributing to Python Code Validator!
This project is a community effort, and we welcome any contribution, from
fixing a typo to implementing a new feature.

This page provides a more detailed guide for developers looking to contribute code.
For a general overview, please see our `Code of Conduct <https://github.com/Qu1nel/PythonCodeValidator/blob/main/.github/CODE_OF_CONDUCT.md>`_.


Development Workflow
====================

To contribute code, please follow these steps:

1.  **Fork the repository** on GitHub and clone it to your local machine.
2.  **Set up the development environment.** We use `uv` for dependency management.
    The `Makefile` automates the entire process:

    .. code-block:: bash

       make setup

    This will create a virtual environment in `.venv/` and install the project in
    editable mode along with all development dependencies.

3.  **Activate the virtual environment:**

    -  On Linux/macOS: ``source .venv/bin/activate``
    -  On Windows: ``.venv\Scripts\activate``

4.  **Create a new branch** for your feature or bug fix. We recommend a
    naming convention like `feat/my-new-selector` or `fix/linter-bug`.

    .. code-block:: bash

       git checkout -b feat/a-new-feature

5.  **Make your changes.** As you code, please ensure you follow our styleguides.

6.  **Add or update tests.** All new features must be accompanied by tests. All bug
    fixes must include a test that reproduces the bug.

7.  **Update documentation.** If you added or changed functionality, please update
    the relevant documentation pages (e.g., the JSON specification or the API reference).

8.  **Commit your changes** following our commit message conventions (see below).

9.  **Push your branch and open a Pull Request** on GitHub. Fill out the PR
    template to help us review your contribution.

Styleguides
===========

Git Commit Messages
-------------------

We follow the `Conventional Commits <https://www.conventionalcommits.org/>`_
specification. This helps us automate versioning and changelogs. Please structure
your commit messages accordingly.

**Format:** `<type>[optional scope]: <description>`

-  **`feat`**: A new feature.
-  **`fix`**: A bug fix.
-  **`docs`**: Documentation only changes.
-  **`style`**: Changes that do not affect the meaning of the code (formatting).
-  **`refactor`**: A code change that neither fixes a bug nor adds a feature.
-  **`test`**: Adding missing tests or correcting existing tests.
-  **`chore`**: Changes to the build process or auxiliary tools.


Python Code Style
-----------------

Our codebase is automatically formatted and linted using **Ruff**. Before
committing, please run:

.. code-block:: bash

   make lint

This command will format your code and check for any style violations.

Testing and Coverage
====================

This project maintains a high standard of test coverage.

-  **Run the full test suite:**

   .. code-block:: bash

      make test

-  **Generate an interactive HTML coverage report:**

   .. code-block:: bash

      make coverage-html

   This will create a report in the `htmlcov/` directory. All Pull Requests must
   pass all tests and should not decrease the overall test coverage.

Architecture Overview
=====================

For a deep dive into the project's architecture, including how Selectors,
Constraints, and Factories work together, please see the
`Developer's Guide <https://github.com/Qu1nel/PythonCodeValidator/blob/main/docs/how_it_works/index.md>`_.