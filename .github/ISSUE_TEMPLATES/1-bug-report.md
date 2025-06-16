name: "Bug Report"
description: "Report an issue to help the project improve."
title: "[Bug] A brief, descriptive title"
labels: ["Type: Bug"]
assignees:

- Qu1nel
  body:
- type: markdown
  attributes:
  value: |
  Thank you for taking the time to fill out this bug report!
- type: textarea
  id: description
  attributes:
  label: Describe the bug
  description: A clear and concise description of what the bug is.
  placeholder: "When I run the validator with rule X on code Y, it incorrectly returns True..."
  validations:
  required: true
- type: textarea
  id: reproduction
  attributes:
  label: To Reproduce
  description: Please provide a minimal JSON rule and a minimal Python code snippet that reproduces the behavior.
  placeholder: |
  1. JSON Rule: `{ "rule_id": 1, "check": { ... } }`
  2. Python Code: `def my_func(): ...`
  3. Command: `validate-code solution.py rules.json`
  4. See error...
  validations:
  required: true
- type: textarea
  id: expected
  attributes:
  label: Expected Behavior
  description: A clear and concise description of what you expected to happen.
  validations:
  required: true
- type: input
  id: version
  attributes:
  label: Validator Version
  description: "What version of `python-code-validator` are you using? (e.g., 0.1.0)"
  validations:
  required: true
- type: dropdown
  id: os
  attributes:
  label: Operating System
  multiple: true
  options:
  - Windows
  - macOS
  - Linux
- type: textarea
  id: context
  attributes:
  label: Additional Context
  description: Add any other context about the problem here (screenshots, logs, etc.).