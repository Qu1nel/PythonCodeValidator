.. _spec_constraints:

***********
Constraints
***********

Constraints are the part of a "full" rule that defines **what condition** the
nodes found by a selector must satisfy. Each constraint takes a list of AST
nodes and returns ``true`` if the condition is met, or ``false`` otherwise.


---

Constraint Reference
====================

.. _spec_constraint_is_required:

is_required
-----------
Checks that the selector found at least one matching node. This is the most
common constraint to enforce the presence of a required code element.

**JSON `type`**: ``"is_required"``

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``count``
     - integer, *optional*
     - If provided, requires the number of found nodes to be exactly this value.

**Example:**
Ensure that exactly one function named `main` was found.
.. code-block:: json

   "constraint": {
     "type": "is_required",
     "count": 1
   }

---

.. _spec_constraint_is_forbidden:

is_forbidden
------------
Checks that the selector found **zero** matching nodes. This is used to
forbid certain language constructs or library uses.

**JSON `type`**: ``"is_forbidden"``
**Parameters**: None.

**Example:**
Ensure that the `eval` function is never called.
.. code-block:: json

   "constraint": { "type": "is_forbidden" }

---

.. _spec_constraint_must_inherit_from:

must_inherit_from
-----------------
Checks that a class (found by a `class_def` selector) inherits from a
specific parent class. This works for both simple names and fully-qualified names.

**JSON `type`**: ``"must_inherit_from"``

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``parent_name``
     - string, **required**
     - The expected name of the parent class (e.g., ``"Exception"``, ``"arcade.Window"``).

**Example:**
Ensure the `MyGame` class inherits from `arcade.Window`.
.. code-block:: json

   "constraint": {
     "type": "must_inherit_from",
     "parent_name": "arcade.Window"
   }

---

.. _spec_constraint_must_be_type:

must_be_type
------------
Checks the type of the value in an assignment statement. It works for simple
literals (numbers, strings) and for calls to built-in type constructors
(e.g., `list()`, `dict()`).

**JSON `type`**: ``"must_be_type"``

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``expected_type``
     - string, **required**
     - The name of the required type. Supported: ``"str"``, ``"int"``, ``"float"``, ``"list"``, ``"dict"``, ``"bool"``, ``"set"``, ``"tuple"``.

**Example:**
Ensure a global constant `MAX_RETRIES` is an integer.
.. code-block:: json

   "constraint": {
     "type": "must_be_type",
     "expected_type": "int"
   }

---

.. _spec_constraint_must_have_args:

must_have_args
--------------
Checks that a function or method has a specific signature.

**JSON `type`**: ``"must_have_args"``

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``count``
     - integer, *optional*
     - The exact number of required arguments (excluding `self`/`cls`).
   * - ``names``
     - list[str], *optional*
     - A list of exact argument names in the correct order.
   * - ``exact_match``
     - boolean, *optional*
     - Used with `names`. If ``false``, only checks for presence, not order or exact count. Defaults to ``true``.

**Example:**
Ensure the `__init__` method accepts `width` and `height`.
.. code-block:: json

   "constraint": {
     "type": "must_have_args",
     "names": ["width", "height"]
   }

---

.. _spec_constraint_name_must_be_in:

name_must_be_in
---------------
Checks if the name of each found node is present in an allowed list of names.
Useful for restricting variable or function names.

**JSON `type`**: ``"name_must_be_in"``

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``allowed_names``
     - list[str], **required**
     - A list of strings containing the allowed names.

**Example:**
Ensure all global variables are from a pre-approved list of constants.
.. code-block:: json

   "constraint": {
     "type": "name_must_be_in",
     "allowed_names": ["SCREEN_WIDTH", "SCREEN_HEIGHT", "TITLE"]
   }

---

.. _spec_constraint_value_must_be_in:

value_must_be_in
----------------
Checks if the value of each found literal node is in an allowed list. This is
the primary tool for forbidding "magic numbers" or "magic strings".

**JSON `type`**: ``"value_must_be_in"``

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``allowed_values``
     - list, **required**
     - A list of allowed literal values (e.g., ``[0, 1]``, ``["OK", "ERROR"]``).

**Example:**
Allow only specific status codes to be used as literals.
.. code-block:: json

   "constraint": {
     "type": "value_must_be_in",
     "allowed_values": [200, 404, 500]
   }