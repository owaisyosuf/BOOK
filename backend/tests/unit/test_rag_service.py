import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.rag_service import RAGService


@pytest.fixture
def rag_service():
    with patch('src.services.rag_service.ChatOpenAI') as mock_chat_model, \
         patch('src.services.rag_service.ChatPromptTemplate') as mock_prompt:
        # Mock the chat model
        mock_chat_model.return_value = AsyncMock()
        mock_chat_model.return_value.agenerate.return_value = MagicMock()
        mock_chat_model.return_value.agenerate.return_value.generations = [[MagicMock(text="Test response")]]

        # Mock the prompt
        mock_prompt_instance = AsyncMock()
        mock_prompt_instance.format_messages.return_value = []
        mock_prompt.return_value = mock_prompt_instance

        service = RAGService()
        service.chat_model = mock_chat_model.return_value
        service.rag_prompt = mock_prompt_instance

        return service


@pytest.mark.asyncio
async def test_process_query_success(rag_service):
    """Test successful query processing"""
    with patch.object(rag_service, 'embedding_service') as mock_embedding:
        mock_embedding.search_similar.return_value = [
            {
                "content": "Test context content",
                "metadata": {"page_path": "/docs/test", "position": 10},
                "similarity_score": 0.8
            }
        ]

        result = await rag_service.process_query("Test question")

        assert result["status"] == "success"
        assert "response" in result
        assert "citations" in result


@pytest.mark.asyncio
async def test_process_query_not_found(rag_service):
    """Test query processing when no relevant context is found"""
    with patch.object(rag_service, 'embedding_service') as mock_embedding:
        mock_embedding.search_similar.return_value = []

        result = await rag_service.process_query("Test question")

        assert result["status"] == "not_found"
        assert result["response"] == "Information not found in the book content."
        assert result["citations"] == []


@pytest.mark.asyncio
async def test_process_query_low_similarity(rag_service):
    """Test query processing when context has low similarity"""
    with patch.object(rag_service, 'embedding_service') as mock_embedding:
        mock_embedding.search_similar.return_value = [
            {
                "content": "Test context content",
                "metadata": {"page_path": "/docs/test", "position": 10},
                "similarity_score": 0.1  # Below threshold
            }
        ]

        result = await rag_service.process_query("Test question")

        assert result["status"] == "not_found"
        assert result["response"] == "Information not found in the book content."
        assert result["citations"] == []


@pytest.mark.asyncio
async def test_process_query_error_handling(rag_service):
    """Test query processing error handling"""
    with patch.object(rag_service, 'embedding_service') as mock_embedding:
        mock_embedding.search_similar.side_effect = Exception("Test error")

        result = await rag_service.process_query("Test question")

        assert result["status"] == "error"
        assert "response" in result
        assert "citations" in result
        assert result["citations"] == []