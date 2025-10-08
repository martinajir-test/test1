# Integration Tests

This directory contains integration tests for the repository.

## Running Tests

To run the integration tests:

```bash
./tests/integration_test.sh
```

## Test Coverage

The integration tests validate:
- Repository structure (required files exist)
- Markdown files are not empty
- GitHub workflow configuration exists
- Content contains expected keywords
- Markdown formatting is correct

## Requirements

- Bash shell
- Standard Unix utilities (grep, test)

## Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed
