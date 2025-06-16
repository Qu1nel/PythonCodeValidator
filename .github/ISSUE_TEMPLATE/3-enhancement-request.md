name: "Enhancement Request"
description: "Suggest an improvement for an existing feature."
title: "[Enhancement] A brief title for the improvement"
labels: ["Type: Enhancement"]
assignees:

- Qu1nel
  body:
- type: markdown
  attributes:
  value: "Thanks for helping us improve the project!"
- type: textarea
  id: enhancement-description
  attributes:
  label: What part of the project would you like to see enhanced?
  description: "Please provide a clear description of the existing feature and why it should be improved."
  placeholder: "The `must_have_args` constraint is great, but it would be even better if it could..."
  validations:
  required: true
- type: textarea
  id: proposed-solution
  attributes:
  label: Describe the proposed enhancement
  description: "A clear and concise description of how you'd like it to work."