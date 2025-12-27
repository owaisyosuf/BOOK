#!/usr/bin/env python3
"""
Simple test to verify the project structure is correct
"""

import sys
import os

# Add the backend src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

print("Testing basic imports...")

try:
    # Test basic imports that don't require external dependencies
    from config.settings import settings
    print("✓ Settings module imported successfully")
except ImportError as e:
    print(f"✗ Settings import failed: {e}")

try:
    # Test model imports
    from models.book_content import BookContent
    print("✓ BookContent model imported successfully")
except ImportError as e:
    print(f"✗ BookContent import failed: {e}")

try:
    # Test that the directory structure is correct
    import os
    expected_dirs = [
        'backend/src/models',
        'backend/src/services',
        'backend/src/api',
        'backend/src/api/routes',
        'frontend/docs',
        'frontend/src/components/Chatbot',
        'frontend/src/components/Book'
    ]

    all_exist = True
    for dir_path in expected_dirs:
        if not os.path.exists(dir_path):
            print(f"✗ Directory missing: {dir_path}")
            all_exist = False
        else:
            print(f"✓ Directory exists: {dir_path}")

    if all_exist:
        print("✓ All expected directories exist")

except Exception as e:
    print(f"✗ Directory check failed: {e}")

print("\nProject structure verification complete!")