#!/bin/bash
# Simple test script to validate repository content

echo "Running tests..."

# Test 1: Check if README.md exists
if [ -f "README.md" ]; then
    echo "✓ README.md exists"
else
    echo "✗ README.md not found"
    exit 1
fi

# Test 2: Check if test.md exists
if [ -f "test.md" ]; then
    echo "✓ test.md exists"
else
    echo "✗ test.md not found"
    exit 1
fi

echo "All tests passed!"
exit 0
