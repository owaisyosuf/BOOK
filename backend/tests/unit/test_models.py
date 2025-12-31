import pytest
from datetime import datetime
from src.models.book_content import BookContent, BookContentCreate
from src.models.query import QueryModel, QueryCreate


def test_book_content_model():
    """Test BookContent model creation and validation"""
    content = BookContent(
        id="test-id",
        title="Test Title",
        content="This is test content for the book",
        section="Chapter 1",
        page_path="/docs/test",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1
    )

    assert content.id == "test-id"
    assert content.title == "Test Title"
    assert content.content == "This is test content for the book"
    assert content.section == "Chapter 1"
    assert content.page_path == "/docs/test"
    assert content.version == 1


def test_book_content_create_model():
    """Test BookContentCreate model validation"""
    content_create = BookContentCreate(
        title="Test Title",
        content="This is test content for the book",
        section="Chapter 1",
        page_path="/docs/test"
    )

    assert content_create.title == "Test Title"
    assert content_create.content == "This is test content for the book"
    assert content_create.section == "Chapter 1"
    assert content_create.page_path == "/docs/test"


def test_query_model():
    """Test QueryModel creation and validation"""
    query = QueryModel(
        id="test-query-id",
        query_text="What is RAG?",
        user_id="user-123",
        scope="full_book",
        created_at=datetime.now()
    )

    assert query.id == "test-query-id"
    assert query.query_text == "What is RAG?"
    assert query.user_id == "user-123"
    assert query.scope == "full_book"


def test_query_create_model():
    """Test QueryCreate model validation"""
    query_create = QueryCreate(
        query_text="What is RAG?",
        scope="full_book"
    )

    assert query_create.query_text == "What is RAG?"
    assert query_create.scope == "full_book"
    assert len(query_create.query_text) >= 3  # Minimum length validation