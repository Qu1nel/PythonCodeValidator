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


Deprecated
----------

- *...*


Removed
-------

- *...*


Fixed
-----

- *...*


Security
--------

- *...*



v0.4.0 - 2025-08-06
===================

Added
-----

- **[feat:typo] Smart typo detection system** - Added comprehensive typo detection infrastructure with TypoDetector, ScopeAnalyzer, and PythonStyleFormatter classes
- **[feat:typo] Levenshtein Distance algorithm** - Implemented string similarity algorithm for basic typo detection with optimized space complexity
- **[feat:typo] Python 3.11+ style error messages** - Added formatted error messages with file location, source highlighting, and typo suggestions
- **[feat:typo] Semantic similarity scoring** - Enhanced confidence calculation with prefix/suffix matching and contextual relevance analysis
- **[feat:typo] Integration with IsRequiredConstraint** - Automatic typo suggestions when validation rules fail to find required elements
- **[feat:ux] Enhanced error reporting with numbered messages** - Added numbered error messages (1., 2., 3.) for better readability
- **[feat:ux] User-visible typo suggestions** - Typo suggestions now appear in user output instead of debug logs only
- **[feat:ux] Compact Russian typo format** - Created user-friendly Russian format for typo suggestions with proper indentation


Fixed
-----

- **[Critical Bug]** Fixed scope validation bug where selectors were not receiving proper scope configuration from the factory, causing rules to search in wrong scopes or ignore scope restrictions entirely.
- **[Scope Logic]** Improved global scope handling for different selector types: assignments now only search at module level, while function calls include ``if __name__ == "__main__"`` blocks.
- **[fix:typo] Improved target type inference** - Enhanced logic for determining whether to search for assignments, functions, or classes based on naming patterns
- **[fix:typo] Enhanced confidence scoring** - Improved similarity scoring algorithm with semantic context awareness for better typo suggestions



v0.3.0 - 2025-07-19
===================

Added
-----

- Added the command line option ``--max-messages N`` to limit the number of error messages displayed.
- Added the command line option ``-x, --exit-on-first-error`` for immediate exit after the first detected error.


Changed
-------

- **[Breaking Change]** The "``--stop-on-first-fail`` option has been renamed to ``--exit-on-first-error``" for greater clarity.


Removed
-------

- **[Breaking Change]** The ``--stop-on-first-fail`` command line option has been removed.


Fixed
-----

- Improved handling of critical errors such as missing file. Now the application displays a clear message to the user instead of crashing with an error, and detailed debugging information is saved in the logs.



v0.2.1 - 2025-07-19
===================

Changed
-------

- *The internal logic of creating rules has been optimized:* Redundant configuration conversion has been eliminated, making the process more efficient.



v0.2.0 - 2025-07-19
===================

Added
-----

- Added the command line option `--no-verdict` to hide the final verdict when displaying validation results.
- A new `TRACE` level has been added to the logging system for more detailed debugging.

Changed
-------

- **[Breaking Change]** The command line argument for controlling the logging level `--log-level` has been renamed to `--log`.
- The logging system has been improved: the message format has been updated for better readability, and the default level has been changed to `ERROR`.

Removed
-------

- **[Breaking Change]** The `--silent` command line option has been removed. To suppress the output, you should now use the new `--quiet` option.



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