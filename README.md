# test1

A test repository for GitHub Actions and workflow experimentation.

## Overview

This repository serves as a testing ground for various GitHub Actions workflows and automation features. It contains sample workflows demonstrating CI/CD patterns and approval mechanisms.

## Features

- **Continuous Integration**: Automated builds and tests on push and pull requests
- **PR Approval Workflow**: Demonstrates environment-based approval requirements for pull requests
- **Manual Workflow Dispatch**: Support for manually triggered workflows

## GitHub Actions Workflows

This repository includes the following workflows:

### CI Workflow (`blank.yml`)
- Triggers on push and pull requests to the `main` branch
- Runs deployment and build jobs
- Can be manually triggered via workflow_dispatch

### PR Approval Workflow (`pr-approval.yml`)
- Requires approval before running on pull requests
- Uses the `pr-approval` environment (configured in repository settings)
- Demonstrates protected environment patterns

## Getting Started

This is a test repository. To use it as a reference:

1. Clone the repository
   ```bash
   git clone https://github.com/martinajir-test/test1.git
   cd test1
   ```

2. Explore the workflows in `.github/workflows/`

3. Review the workflow configurations and adapt them for your needs

## Contributing

This is a test repository primarily for experimentation. Feel free to fork and modify for your own testing purposes.

## License

This is a test repository without a specific license.
