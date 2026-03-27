# test1

## Overview

test1 is a test repository for exploring GitHub features, workflows, and automation capabilities. This repository demonstrates various GitHub Actions workflows including continuous integration (CI) and pull request approval processes.

### Key Features

- **GitHub Actions Workflows**: Automated CI/CD pipelines with deployment and build jobs
- **PR Approval System**: Enforces review requirements before pull request execution
- **Issue Templates**: Standardized bug report templates for consistent issue tracking

## Installation

This repository is primarily for demonstration and testing purposes. To use or contribute to this repository:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/martinajir-test/test1.git
   cd test1
   ```

2. **Explore the workflows**:
   - GitHub Actions workflows are located in `.github/workflows/`
   - Review the CI workflow in `blank.yml`
   - Check the PR approval workflow in `pr-approval.yml`

## Usage

### Running Workflows

The repository includes several GitHub Actions workflows:

- **CI Workflow**: Automatically runs on push to main branch or pull requests
  - Performs deployment jobs
  - Executes build and test steps
  
- **PR Approval Workflow**: Requires approval before running on pull requests
  - Configured in repository settings
  - Uses the `pr-approval` environment

### Creating Issues

Use the provided issue templates when reporting bugs:
- Navigate to the Issues tab
- Click "New Issue"
- Select the "Bug Report" template
- Fill in the required information

## Contributing

We welcome contributions to this repository! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and commit them with clear, descriptive messages
4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** against the main branch
6. **Wait for review** - the PR approval workflow will require approval before execution

### Contribution Guidelines

- Follow existing code and documentation style
- Test your changes thoroughly
- Provide clear descriptions in pull requests
- Be respectful and constructive in discussions

## Support

If you encounter any issues or have questions:

- **Report Bugs**: Use the [Bug Report issue template](../../issues/new?template=bug_report.yml)
- **General Questions**: Open a new [Discussion](../../discussions) or [Issue](../../issues)
- **Contact**: Reach out to the repository maintainers

## License

This is a test repository. Please check with the repository owner for licensing information.

---

**Note**: This is a test repository maintained by martinajir-test for demonstration and experimentation purposes.
