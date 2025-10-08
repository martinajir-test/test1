#!/bin/bash
# Integration tests for the repository

set -e  # Exit on error

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    echo -e "${GREEN}✓${NC} $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

fail_test() {
    echo -e "${RED}✗${NC} $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

echo "Running integration tests..."
echo "=============================="

# Test 1: Check if README.md exists
echo "Test 1: Checking if README.md exists..."
if [ -f "README.md" ]; then
    pass_test "README.md exists"
else
    fail_test "README.md does not exist"
fi

# Test 2: Check if test.md exists
echo "Test 2: Checking if test.md exists..."
if [ -f "test.md" ]; then
    pass_test "test.md exists"
else
    fail_test "test.md does not exist"
fi

# Test 3: Check if README.md is not empty
echo "Test 3: Checking if README.md is not empty..."
if [ -s "README.md" ]; then
    pass_test "README.md is not empty"
else
    fail_test "README.md is empty"
fi

# Test 4: Check if test.md is not empty
echo "Test 4: Checking if test.md is not empty..."
if [ -s "test.md" ]; then
    pass_test "test.md is not empty"
else
    fail_test "test.md is empty"
fi

# Test 5: Check if GitHub workflow exists
echo "Test 5: Checking if GitHub workflow exists..."
if [ -f ".github/workflows/blank.yml" ]; then
    pass_test "GitHub workflow exists"
else
    fail_test "GitHub workflow does not exist"
fi

# Test 6: Validate README.md contains expected content
echo "Test 6: Checking if README.md contains 'test' keyword..."
if grep -q "test" "README.md"; then
    pass_test "README.md contains 'test' keyword"
else
    fail_test "README.md does not contain 'test' keyword"
fi

# Test 7: Validate test.md has proper markdown header
echo "Test 7: Checking if test.md has level 2 markdown header..."
if grep -q "^##" "test.md"; then
    pass_test "test.md has level 2 markdown header"
else
    fail_test "test.md does not have level 2 markdown header"
fi

# Summary
echo ""
echo "=============================="
echo "Test Summary:"
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"
echo "=============================="

if [ $TESTS_FAILED -gt 0 ]; then
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
