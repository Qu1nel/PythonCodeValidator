.. _faq:

***************************
Frequently Asked Questions
***************************


General
=======

**Q: What is the difference between this validator and a standard linter like Ruff or Flake8?**

A: Linters like Ruff and Flake8 are excellent for checking code *style* and finding common programming *errors* (like unused variables). The Python Code Validator is designed to check for **structural and logical requirements** specific to a learning task. For example, you can enforce that a student *must* use a `for` loop, *must not* use `eval()`, or that a class *must* inherit from a specific parent. It complements, rather than replaces, a standard linter.

**Q: Can I use this for languages other than Python?**

A: No. The validator is deeply integrated with Python's Abstract Syntax Tree (AST) and is designed exclusively for analyzing Python source code.

**Q: Is the validator secure? Can it execute student code?**

A: The validator performs **static analysis only**. It never executes the student's code. This makes it completely safe to run on untrusted code. It parses the code into a data structure (the AST) and analyzes that structure.

Writing Rules
=============

**Q: My `check_linter_pep8` rule passes even though the code has style errors. Why?**

A: By default, the `flake8` check might use a conservative set of rules. To ensure all issues are caught, you can either pass an empty `ignore` list or a specific `select` list in the rule's `params`.

.. code-block:: json

   {
     "rule_id": 1,
     "type": "check_linter_pep8",
     "message": "Enforcing strict PEP8.",
     "params": {
       "select": ["E", "W", "F"]
     }
   }


**Q: How do I check for something inside a specific method of a class?**

A: Use the ``in_scope`` modifier in your selector. This is one of the most powerful features of the validator.

.. code-block:: json

   "selector": {
     "type": "function_call",
     "name": "print",
     "in_scope": {
       "class": "MyGame",
       "method": "update"
     }
   }

This will only find `print()` calls that are inside the `update` method of the `MyGame` class.

**Q: What's the difference between `assignment` and `usage` selectors?**

A: The `assignment` selector finds where a variable is **written to** (e.g., `x = 5`). The `usage` selector finds where a variable's value is **read from** (e.g., `y = x + 1`).