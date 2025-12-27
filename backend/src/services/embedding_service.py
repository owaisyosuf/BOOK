import openai
from typing import List, Dict, Any
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key
        )

        # Initialize Qdrant client
        self.qdrant_client = Qdrant(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            collection_name="book_content",
            embeddings=self.embeddings
        )

    async def create_embeddings(self, text: str) -> List[float]:
        """
        Create embeddings for a given text
        """
        try:
            embedding = await self.embeddings.aembed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise

    async def store_content(self, content_id: str, text: str, metadata: Dict[str, Any]) -> bool:
        """
        Store content with its embeddings in Qdrant
        """
        try:
            # Add document to Qdrant
            self.qdrant_client.add_texts(
                texts=[text],
                metadatas=[metadata],
                ids=[content_id]
            )
            return True
        except Exception as e:
            logger.error(f"Error storing content in Qdrant: {str(e)}")
            return False

    async def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar content based on query
        """
        try:
            # Search in Qdrant
            results = self.qdrant_client.similarity_search_with_score(
                query,
                k=top_k
            )

            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": score
                })

            return formatted_results
        except Exception as e:
            logger.error(f"Error searching similar content: {str(e)}")
            return []

    async def delete_content(self, content_id: str) -> bool:
        """
        Delete content from Qdrant
        """
        try:
            self.qdrant_client.delete([content_id])
            return True
        except Exception as e:
            logger.error(f"Error deleting content from Qdrant: {str(e)}")
            return False