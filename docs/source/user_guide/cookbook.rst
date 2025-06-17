.. _cookbook:

********
Cookbook
********

This page contains a collection of practical examples ("recipes") for common
validation tasks. Use these as a starting point for writing your own rules.

General Checks
==============

How to require a specific function?
-----------------------------------
Use the ``function_def`` selector with the ``is_required`` constraint.

.. code-block:: json

   {
     "rule_id": 101,
     "message": "Required function 'solve' is missing.",
     "check": {
       "selector": { "type": "function_def", "name": "solve" },
       "constraint": { "type": "is_required" }
     }
   }

How to forbid a specific function call (e.g., `eval`)?
-------------------------------------------------------
Use the ``function_call`` selector with the ``is_forbidden`` constraint.

.. code-block:: json

   {
     "rule_id": 102,
     "message": "The use of 'eval()' is forbidden.",
     "check": {
       "selector": { "type": "function_call", "name": "eval" },
       "constraint": { "type": "is_forbidden" }
     }
   }

How to check for PEP8 compliance?
---------------------------------
Use the ``check_linter_pep8`` short rule. You can optionally provide
a list of error codes to ignore.

.. code-block:: json

   {
     "rule_id": 103,
     "type": "check_linter_pep8",
     "message": "Code does not adhere to PEP8 style guidelines.",
     "params": {
       "ignore": ["E501", "W292"]
     }
   }


Working with Functions and Methods
==================================

How to check the number of arguments in a function?
----------------------------------------------------
Use the ``must_have_args`` constraint with the ``count`` parameter. This checks
arguments excluding `self` or `cls` in methods.

.. code-block:: json

   {
     "rule_id": 201,
     "message": "Function 'calculate' must accept exactly 2 arguments.",
     "check": {
       "selector": { "type": "function_def", "name": "calculate" },
       "constraint": { "type": "must_have_args", "count": 2 }
     }
   }

How to check for specific argument names in a method?
------------------------------------------------------
Use ``must_have_args`` with the ``names`` parameter. Note that you do not
need to include `self`.

.. code-block:: json

   {
     "rule_id": 202,
     "message": "The __init__ method must accept 'width' and 'height'.",
     "check": {
       "selector": {
         "type": "function_def",
         "name": "__init__",
         "in_scope": { "class": "MyGame" }
       },
       "constraint": {
         "type": "must_have_args",
         "names": ["width", "height"]
       }
     }
   }


Working with Classes and Inheritance
====================================

How to require a class to inherit from another?
-----------------------------------------------
Use the ``must_inherit_from`` constraint. It works for simple names
and fully qualified names.

.. code-block:: json

   {
     "rule_id": 301,
     "message": "Class 'MyGameWindow' must inherit from 'arcade.Window'.",
     "check": {
       "selector": { "type": "class_def", "name": "MyGameWindow" },
       "constraint": {
         "type": "must_inherit_from",
         "parent_name": "arcade.Window"
       }
     }
   }

How to check for an attribute assignment inside `__init__`?
------------------------------------------------------------
Use the ``assignment`` selector scoped to the method.

.. code-block:: json

   {
     "rule_id": 302,
     "message": "The attribute 'self.score' must be initialized in the constructor.",
     "check": {
       "selector": {
         "type": "assignment",
         "name": "self.score",
         "in_scope": { "class": "MyGameWindow", "method": "__init__" }
       },
       "constraint": { "type": "is_required" }
     }
   }


Working with Variables and Literals
===================================

How to forbid "magic numbers" in a specific function?
-----------------------------------------------------
Use the ``literal`` selector with an ``in_scope`` and a ``value_must_be_in``
constraint. This rule checks for any numbers other than 0 or 1 inside the
`update` method.

.. code-block:: json

   {
     "rule_id": 401,
     "message": "Do not use magic numbers in the update method. Use constants.",
     "check": {
       "selector": {
         "type": "literal",
         "name": "number",
         "in_scope": { "function": "update" }
       },
       "constraint": {
         "type": "value_must_be_in",
         "allowed_values": [0, 1]
       }
     }
   }

How to ensure all global variables are named like CONSTANTS?
-------------------------------------------------------------
This requires a more advanced technique. We can't do this with a single rule yet,
but it shows the direction for future extensions. A potential future rule might look
like this:

.. code-block:: json
   :emphasize-lines: 5-8

   {
     "rule_id": 402,
     "message": "Global constants must be named in UPPER_SNAKE_CASE.",
     "check": {
       "selector": { "type": "assignment", "in_scope": "global" },
       "constraint": {
         "type": "name_matches_regex",
         "pattern": "^[A-Z0-9_]+$"
       }
     }
   }

.. note::
   The ``name_matches_regex`` constraint is an example of a potential future
   enhancement and is not yet implemented.