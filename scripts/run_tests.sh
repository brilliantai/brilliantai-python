#!/bin/bash
set -e

echo "Running Ruff linting..."
ruff check .

echo "Running tests with coverage..."
python -m pytest

echo "All tests completed successfully!"
