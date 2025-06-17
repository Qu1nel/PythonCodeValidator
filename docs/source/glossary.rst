.. _glossary:

********
Glossary
********

.. glossary::
   :sorted:

   AST (Abstract Syntax Tree)
      A tree representation of the abstract syntactic structure of source code.
      The validator parses Python code into an AST and then analyzes this tree,
      rather than the raw text.

   Rule
      A single validation check defined in a JSON file. It consists of a
      ``rule_id``, a ``message``, and either a pre-defined ``type`` (a "short"
      rule) or a ``check`` block (a "full" rule).

   Selector
      The part of a "full" rule that specifies **what** to find in the code's
      AST. For example, a `function_def` selector finds all function
      definitions.

   Constraint
      The part of a "full" rule that specifies **what condition** the nodes
      found by a selector must satisfy. For example, an `is_required`
      constraint checks that the selector found at least one node.

   Scope
      The specific region of code where a rule should be applied. This can be
      "global", a specific function, a class, or a method within a class. It is
      defined using the ``in_scope`` key in a selector.

   Validator
      The core engine of this project. It is responsible for parsing the source
      code and the JSON rules, and then executing the rules to check for
      violations.

   Checker
      A term used to describe the tools for **dynamic testing** (which are
      separate from this static validator). Checkers execute code to verify
      its behavior, whereas the validator only analyzes its structure.