name: "Feature Request"
description: "Suggest an idea for a new feature."
title: "[Feature] A brief title for your idea"
labels: ["Type: Feature"]
assignees:

- Qu1nel
  body:
- type: markdown
  attributes:
  value: "Thank you for suggesting a new feature! Please provide as much detail as possible."
- type: textarea
  id: problem-description
  attributes:
  label: Is your feature request related to a problem?
  description: "A clear and concise description of what the problem is. Ex. I'm always frustrated when..."
  placeholder: "It's currently difficult to validate X because there is no selector for Y."
  validations:
  required: true
- type: textarea
  id: solution-description
  attributes:
  label: Describe the solution you'd like
  description: "A clear and concise description of what you want to happen."
  placeholder: "I would like a new selector `{ \"type\": \"new_selector\" }` that finds..."
- type: textarea
  id: alternatives
  attributes:
  label: Describe alternatives you've considered
  description: "A clear and concise description of any alternative solutions or features you've considered."