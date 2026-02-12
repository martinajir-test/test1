#!/bin/bash
set -e

# Simple test script
echo "Running tests..."

# Test 1: Check if README.md exists
if [ -f "README.md" ]; then
    echo "✓ Test 1 passed: README.md exists"
else
    echo "✗ Test 1 failed: README.md not found"
    exit 1
fi

# Test 2: Check if test.md exists
if [ -f "test.md" ]; then
    echo "✓ Test 2 passed: test.md exists"
else
    echo "✗ Test 2 failed: test.md not found"
    exit 1
fi

echo "All tests passed!"
exit 0
