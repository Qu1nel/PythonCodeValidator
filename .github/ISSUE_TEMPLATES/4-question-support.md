name: "Other Issue or Question"
description: "Report a documentation error, a failing test, or ask a question."
title: "[Docs/Test/Question] A brief, descriptive title"
labels: ["Documentation", "Type: Test", "Type: Question"]
assignees:

- Qu1nel
  body:
- type: dropdown
  id: issue-type
  attributes:
  label: What type of issue is this?
  options:
    - Documentation Issue
    - Failing Test Report
    - Question or Support Request
      validations:
      required: true
- type: textarea
  id: description
  attributes:
  label: Please describe the issue or your question in detail
  description: "If it's a bug, please include steps to reproduce. If it's a question, be as specific as possible."
  validations:
  required: true