#!/bin/bash
# Script to run tests for the Mergington High School API

echo "Running FastAPI tests with pytest..."
echo "=================================="

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

echo ""
echo "Test run complete!"
echo "Coverage report saved to htmlcov/index.html"