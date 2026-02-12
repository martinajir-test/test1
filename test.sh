#!/bin/bash
# Simple test script

set -e

echo "Running tests..."

# Test 1: Check if README.md exists
echo "Test 1: Checking if README.md exists..."
if [ -f "README.md" ]; then
    echo "✓ README.md exists"
else
    echo "✗ README.md not found"
    exit 1
fi

# Test 2: Check if test.md exists
echo "Test 2: Checking if test.md exists..."
if [ -f "test.md" ]; then
    echo "✓ test.md exists"
else
    echo "✗ test.md not found"
    exit 1
fi

# Test 3: Basic content check
echo "Test 3: Checking README.md has content..."
if [ -s "README.md" ]; then
    echo "✓ README.md has content"
else
    echo "✗ README.md is empty"
    exit 1
fi

echo ""
echo "All tests passed! ✓"
