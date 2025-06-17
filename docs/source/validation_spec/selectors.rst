.. _spec_selectors:

*********
Selectors
*********

Selectors are the part of a "full" rule that defines **what** to find in the
source code's Abstract Syntax Tree (AST). Each selector is configured with a
``type`` and can be modified with additional parameters to refine the search.

---

Common Parameters
=================

Most selectors accept the following optional parameter to narrow the search scope.

in_scope
--------
Limits the search to a specific part of the code.

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - JSON Value
     - Description
   * - ``"global"``
     - Searches only the top-level module scope.
   * - ``{ "function": "my_func" }``
     - Searches only inside the function `my_func`.
   * - ``{ "class": "MyClass" }``
     - Searches only inside the body of class `MyClass` (excluding its methods).
   * - ``{ "class": "MyClass", "method": "my_method" }``
     - Searches only inside the method `my_method` of class `MyClass`.

**Example:**
To find ``print`` calls only inside the `main` function:

.. code-block:: json

   "selector": {
     "type": "function_call",
     "name": "print",
     "in_scope": { "function": "main" }
   }

---

Selector Reference
==================

.. _spec_selector_function_def:

function_def
------------
Finds function definitions (`def` statements), including methods inside classes.

**JSON ``type``**: ``"function_def"``

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - string
     - The name of the function to find. Use ``"*"`` as a wildcard to find all functions in the given scope.

**Example:**
Find the definition of a function named `solve`.

.. code-block:: json

   "selector": {
     "type": "function_def",
     "name": "solve"
   }


.. _spec_selector_class_def:

class_def
---------
Finds class definitions (`class` statements).

**JSON ``type``**: ``"class_def"``

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - string
     - The name of the class to find. Use ``"*"`` as a wildcard.

**Example:**
Find the definition of a class named `MyGame`.
.. code-block:: json

   "selector": {
     "type": "class_def",
     "name": "MyGame"
   }


.. _spec_selector_import_statement:

import_statement
----------------
Finds `import` or `from ... import` statements.

:**JSON ``type``**: ``"import_statement"``
:**Parameters**:
.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - string
     - The name of the module. This will match `import os`, `import os.path`, and `from os import path`.

**Example:** Find any import of the `sys` module.
.. code-block:: json

   "selector": {
     "type": "import_statement",
     "name": "sys"
   }


.. _spec_selector_function_call:

function_call
-------------
Finds nodes where a function or method is called.

:**JSON ``type``**: ``"function_call"``
:**Parameters**:
.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - string
     - The full name of the function being called (e.g., ``"print"``, ``"requests.get"``).

**Example:** Find all calls to `arcade.run`.
.. code-block:: json

   "selector": {
     "type": "function_call",
     "name": "arcade.run"
   }


.. _spec_selector_assignment:

assignment
----------
Finds assignment statements where a variable or attribute is being written to. This includes ``=`` and type-annotated assignments like ``x: int = 5``.

:**JSON ``type``**: ``"assignment"``
:**Parameters**:
.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - string
     - The full name of the variable or attribute being assigned to (e.g., ``"my_var"``, ``"self.player_score"``). Use ``"*"`` as a wildcard.

**Example:** Find where the attribute `self.score` is assigned a value.
.. code-block:: json

   "selector": {
     "type": "assignment",
     "name": "self.score"
   }


.. _spec_selector_usage:

usage
-----
Finds nodes where a variable or attribute's value is being read (i.e., used in an expression).

:**JSON ``type``**: ``"usage"``
:**Parameters**:
.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - string
     - The name of the variable or attribute being used.

**Example:** Find all places where the `GLOBAL_CONFIG` variable is used.
.. code-block:: json

   "selector": {
     "type": "usage",
     "name": "GLOBAL_CONFIG"
   }


.. _spec_selector_literal:

literal
-------
Finds literal values (e.g., numbers, strings) in the code. This selector is designed to intelligently ignore docstrings and components of f-strings.

:**JSON ``type``**: ``"literal"``
:**Parameters**:
.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - string
     - The type of literal to find. Supported values: ``"number"`` or ``"string"``.

**Example:** Find all hardcoded numbers in the `calculate` function.
.. code-block:: json

   "selector": {
     "type": "literal",
     "name": "number",
     "in_scope": { "function": "calculate" }
   }


.. _spec_selector_ast_node:

ast_node
--------
A generic, low-level selector for finding any AST node by its class name from the built-in ``ast`` module.

:**JSON ``type``**: ``"ast_node"``
:**Parameters**:
.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``node_type``
     - string or list[str]
     - The name of the AST node class (e.g., ``"While"``, ``"Try"``) or a list of names.

**Example:** Find all `while` and `for` loops in the code.
.. code-block:: json

   "selector": {
     "type": "ast_node",
     "node_type": ["While", "For"]
   }