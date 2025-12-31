import pytest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables"""
    # Set minimal required environment variables for testing
    os.environ.setdefault('OPENAI_API_KEY', 'test-key')
    os.environ.setdefault('QDRANT_URL', 'http://localhost:6333')
    os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')

    yield

    # Cleanup: Remove test environment variables if needed
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    if 'QDRANT_URL' in os.environ:
        del os.environ['QDRANT_URL']
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']