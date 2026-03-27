# test1

A test repository for GitHub Actions and CI/CD workflows.

## Overview

This repository is designed for testing and demonstrating GitHub Actions workflows, including CI/CD pipelines and PR approval processes.

## Workflows

The repository includes the following GitHub Actions workflows:

### CI Workflow (`blank.yml`)

A basic continuous integration workflow that:
- Triggers on push and pull requests to the `main` branch
- Can be manually triggered via workflow_dispatch
- Includes a deployment job with environment approval
- Runs a simple build job that checks out the code and executes test commands

### PR Approval Workflow (`pr-approval.yml`)

A workflow that requires approval before running on pull requests:
- Triggers on PR open, synchronize, and reopen events
- Uses the `pr-approval` environment which requires reviewer approval
- Demonstrates environment-based approval gates for pull requests

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       ├── blank.yml          # CI workflow
│       └── pr-approval.yml    # PR approval workflow
├── README.md                  # This file
└── test.md                    # Test documentation file
```

## Getting Started

This is a test repository. To use the workflows:

1. Clone the repository:
   ```bash
   git clone https://github.com/martinajir-test/test1.git
   cd test1
   ```

2. Create a new branch for your changes:
   ```bash
   git checkout -b your-feature-branch
   ```

3. Make your changes and push to GitHub to trigger the workflows

## Environment Setup

The workflows use the following GitHub environments:
- `test` - Used by the deployment job in the CI workflow
- `pr-approval` - Used to require approval for PR workflows

These environments should be configured in the repository settings with appropriate protection rules and required reviewers.

## Contributing

This is a test repository. Feel free to experiment with different workflow configurations and GitHub Actions features.

## License

This is a test repository for educational and testing purposes.
