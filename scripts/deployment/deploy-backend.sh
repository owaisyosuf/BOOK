#!/bin/bash

# Deployment script for backend API
# This script prepares the backend for deployment to a cloud provider

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting backend deployment preparation..."

# Navigate to backend directory
cd backend

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if requirements installation was successful
if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully!"
else
    echo "Dependency installation failed!"
    exit 1
fi

# Run tests (if they exist)
if [ -f "pytest.ini" ] || [ -d "tests" ]; then
    echo "Running tests..."
    python -m pytest
else
    echo "No tests found, skipping test execution."
fi

# Check for environment variables
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please ensure environment variables are set."
fi

# Prepare for deployment (this would be specific to your deployment target)
echo "Backend deployment preparation complete."
echo "The application is ready for deployment to your preferred cloud platform."
echo "Common deployment options: Railway, Render, AWS, GCP, or Azure."