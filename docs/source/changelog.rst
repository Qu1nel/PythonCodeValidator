*********
Changelog
*********

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. _unreleased:

Unreleased
==========

*This section is for upcoming changes. It will become the next version's release notes.*

Added
-----

- *...*

Changed
-------

- *...*

Fixed
-----

- *...*


----

v0.1.3 - 2025-06-17
===================

Patch changes, fixes, and improvements.

Fixed
-----

- **Logging level**: Wherever the level was specified as a string, the LogLevel structure is used.
- **Clean code**: Delete unnecessary comments from code.
- **Docstring**: Update all docstring in all files.



v0.1.2 - 2025-06-17
===================

A little code refinement.

Changed
-------

- **Typo**: Fix `README.md`: add links and clean file.



v0.1.1 - 2025-06-17
===================

The documentation for ReadTheDocs has been written and the book How It Works has also been completed. Deepwiki is integrated into the repository

**Added:**

- **Documentation**: A resource for Reading The Docs in `docs/source`.
- **How It Works**: How It Works in `docs/how_it_works/index.md`.
- **AI in repository**: Deep wiki by `https://deepwiki.com/Qu1nel/PythonCodeValidator`



v0.1.0 - 2025-06-16
===================

This is the initial public release of the Python Code Validator framework.

**Added:**

- **Core Engine**: Implemented the main `StaticValidator` for orchestrating the validation process.
- **JSON Format**: Designed and implemented the first version of the JSON format for validation rules.
- **Short Rules**: Added support for `check_syntax` and `check_linter_pep8`.
- **Selectors**: Implemented a full suite of selectors (`function_def`, `class_def`, `import_statement`, `assignment`, `usage`, `literal`, `ast_node`).
- **Constraints**: Implemented a full suite of constraints (`is_required`, `is_forbidden`, `must_inherit_from`, `must_be_type`, etc.).
- **Scoping**: Added support for `in_scope` to apply rules to specific functions, classes, and methods.
- **CLI**: Created the `validate-code` command-line interface.
- **Testing**: Established a comprehensive test suite with over 90% code coverage.
- **CI/CD**: Set up a GitHub Actions workflow for automated testing and linting.