.. _spec_general:

*************************************
General Structure & "Short" Rules
*************************************

This page describes the overall structure of a ``validation.json`` file and
details the pre-defined "short" rules available for common checks.


Top-Level Structure
===================

Every validation file is a JSON object with the following top-level keys:

.. code-block:: json

   {
     "file_type": "python",
     "description": "A brief description of this rule set.",
     "validation_rules": [
       // ... array of rule objects ...
     ]
   }

- ``file_type`` (string, **required**): Must be ``"python"``.
- ``description`` (string, *optional*): A human-readable description.
- ``validation_rules`` (array, **required**): An array of one or more rule objects.

Rule Object Structure
=====================

Each object inside the ``validation_rules`` array must contain the following keys:

.. code-block:: json
   :emphasize-lines: 2, 3

   {
     "rule_id": 101,
     "message": "This message is shown if the rule fails.",
     "is_critical": false,
     // ... rule-specific keys for either a "short" or "full" rule
   }

- ``rule_id`` (integer, **required**): A unique identifier for the rule.
- ``message`` (string, **required**): The error message to display upon failure.
- ``is_critical`` (boolean, *optional*): If ``true``, validation halts immediately
  if this rule fails. Defaults to ``false``.

A rule object can be either a "short" rule or a "full" rule.

"Short" Rules (Pre-defined Checks)
==================================

Short rules provide a quick way to perform common checks. They are identified
by a ``"type"`` key.

.. _spec_short_check_syntax:

check_syntax
------------

Checks if the Python code is free of syntax errors. This check is performed
implicitly before any other rules, but including it allows you to define a
custom error message.

:**JSON `type`**: ``"check_syntax"``
:**Parameters**: None.

.. code-block:: json

   {
     "rule_id": 1,
     "type": "check_syntax",
     "message": "Your code has syntax errors. Please fix them to continue."
   }


.. _spec_short_check_linter_pep8:

check_linter_pep8
-----------------

Runs the ``flake8`` linter to check for compliance with the PEP8 style guide.

:   **JSON `type`**: ``"check_linter_pep8"``
:   **Parameters (`params` object)**:

    -   ``ignore`` (list[str], *optional*): A list of `flake8` error codes to ignore (e.g., ``["E501"]``).
    -   ``select`` (list[str], *optional*): A list of `flake8` error codes to check for exclusively.

.. code-block:: json

   {
     "rule_id": 2,
     "type": "check_linter_pep8",
     "message": "Your code does not follow PEP8 style guidelines.",
     "params": {
       "ignore": ["E501", "W292"]
     }
   }

.. note::
   For custom structural checks (e.g., "function `solve` must exist"), you
   must use a "full" rule, which is described in the :doc:`selectors` and
   :doc:`constraints` sections.