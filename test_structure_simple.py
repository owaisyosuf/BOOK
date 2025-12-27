#!/usr/bin/env python3
"""
Simple test to verify the project structure is correct without requiring all dependencies
"""

import sys
import os

print("Testing basic project structure...")

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
            print(f"X Directory missing: {dir_path}")
            all_exist = False
        else:
            print(f"OK Directory exists: {dir_path}")

    if all_exist:
        print("OK All expected directories exist")

    # Test that key files exist
    expected_files = [
        'backend/src/models/book_content.py',
        'backend/src/models/query.py',
        'backend/src/models/response.py',
        'backend/src/services/rag_service.py',
        'backend/src/api/main.py',
        'frontend/docs/intro.md',
        'frontend/docs/getting-started.md',
        'frontend/src/components/Chatbot/ChatInterface.jsx',
        'specs/001-ai-book-rag/tasks.md',
        'specs/001-ai-book-rag/plan.md',
        'specs/001-ai-book-rag/spec.md'
    ]

    all_files_exist = True
    for file_path in expected_files:
        if not os.path.exists(file_path):
            print(f"X File missing: {file_path}")
            all_files_exist = False
        else:
            print(f"OK File exists: {file_path}")

    if all_files_exist:
        print("OK All expected files exist")

except Exception as e:
    print(f"X Structure check failed: {e}")

print("\nProject structure verification complete!")