name: "Bug report"
description: "File a bug report if something isn't working as expected."
title: "[Bug] "
labels: [bug]
body:
  - type: markdown
    attributes:
      value: |
        ## Describe the bug
  - type: textarea
    id: description
    attributes:
      label: "What happened?"
      description: "A clear and concise description of what the bug is."
      placeholder: "Describe the problem here."
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: "Steps to reproduce"
      description: "Please list the steps needed to reproduce the issue."
      placeholder: "List the steps here."
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: "Version"
      description: "What version of the app or codebase are you using?"
      placeholder: "e.g. v1.2.3, commit sha, etc."
  - type: textarea
    id: screenshots
    attributes:
      label: "Screenshots"
      description: "Add screenshots to help explain your problem."
      placeholder: "Paste images or drag and drop here."
  - type: textarea
    id: environment
    attributes:
      label: "Environment"
      description: "OS, Browser, or other environment details."
      placeholder: "e.g. Windows 11, Chrome 120, etc."
  - type: textarea
    id: additional
    attributes:
      label: "Additional context"
      description: "Any other context about the problem here."
      placeholder: "Add any other details, logs, or context here."