#!/bin/bash

# Deployment script for frontend to GitHub Pages
# This script builds the Docusaurus site and prepares it for GitHub Pages deployment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting frontend deployment..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "Installing frontend dependencies..."
npm install

# Build the site
echo "Building the Docusaurus site..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "The site has been built in the build/ directory"
    echo "To deploy to GitHub Pages, run: npm run deploy"
else
    echo "Build failed!"
    exit 1
fi

echo "Frontend deployment preparation complete."