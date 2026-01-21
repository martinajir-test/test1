name: Bug report
description: File a bug report if something isn't working as expected.
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
      label: What happened?
      description: A clear and concise description of what the bug is.
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: Please list the steps needed to reproduce the issue.
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Version
      description: What version of the app or codebase are you using?
  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: Add screenshots to help explain your problem.
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, Browser, or other environment details.
  - type: textarea
    id: additional
    attributes:
      label: Additional context
      description: Any other context about the problem here.
