.. _quickstart:

**********
Quickstart
**********

This guide provides a complete, step-by-step example of how to use the
``validate-code`` tool to check a Python file against a simple set of rules.

The Goal
========

Our goal is to verify that a student's submission file (`solution.py`) contains a
required function named ``solve``, and that it does not use the forbidden `os` module.

Step 1: The Python Code to Validate
====================================

First, let's create a sample Python file that violates our requirements. This
will be our test subject.

.. code-block:: python
   :caption: solution.py
   :emphasize-lines: 1, 3

    import os # This import is not allowed.

    # The required 'solve' function is missing.
    def main():
       print("This program is missing a key function.")

    if __name__ == "__main__":
       main()

Step 2: Creating the JSON Rules File
====================================

Next, we define our validation requirements in a JSON file. Let's call it
``rules.json``. The validator will read this file to know what to check for.

.. code-block:: json
   :caption: rules.json
   :emphasize-lines: 8-18, 20-30

   {
     "description": "Rules for the quickstart example.",
     "validation_rules": [
       {
         "rule_id": 101,
         "message": "Required function 'solve' is missing.",
         "is_critical": true,
         "check": {
           "selector": {
             "type": "function_def",
             "name": "solve"
           },
           "constraint": {
             "type": "is_required"
           }
         }
       },
       {
         "rule_id": 102,
         "message": "The use of the 'os' module is forbidden.",
         "check": {
           "selector": {
             "type": "import_statement",
             "name": "os"
           },
           "constraint": {
             "type": "is_forbidden"
           }
         }
       }
     ]
   }

This file defines two rules:
1.  **Rule 101**: Checks that a function named ``solve`` **is required**. We've marked it as critical.
2.  **Rule 102**: Checks that the ``os`` module **is forbidden**.

Step 3: Running the Validator
=============================

With both files in the same directory, open your terminal and run the
``validate-code`` command:

.. code-block:: bash

   validate-code solution.py rules.json

Step 4: Analyzing the Output
============================

The validator will execute the rules and report the failures. Because we marked
Rule 101 as ``"is_critical": true``, the validation process will stop after
finding the first error.

.. code-block:: text
   :caption: Console Output

   Starting validation for: solution.py
   Required function 'solve' is missing.
   Critical rule failed. Halting validation.
   Validation failed.

The output clearly indicates that the first critical rule failed, and the
process was halted. If we remove ``"is_critical": true``, the validator would
report both errors.

This simple example demonstrates the core workflow. To see more advanced examples
and learn how to write rules for scenarios, head to the :doc:`cookbook`.