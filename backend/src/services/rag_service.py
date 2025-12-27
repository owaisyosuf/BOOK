import logging
from typing import Dict, Any, List, Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import settings
from services.embedding_service import EmbeddingService
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import asyncio

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        # Initialize OpenAI chat model
        self.chat_model = ChatOpenAI(
            openai_api_key=settings.openai_api_key,
            model_name="gpt-3.5-turbo"  # or "gpt-4" depending on your needs
        )

        # Define the prompt template for RAG
        self.rag_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a helpful assistant that answers questions based only on the provided context.
            If the answer is not available in the context, clearly state that the information is not found.
            Always cite the sources from the context when providing answers.
            Do not make up information that is not in the context."""),
            HumanMessage(content="Context: {context}\n\nQuestion: {question}\n\nPlease provide an answer based only on the context above, with citations where appropriate.")
        ])

    async def process_query(
        self,
        query_text: str,
        scope: str = "full_book",
        section: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a query using RAG methodology
        """
        try:
            # Search for relevant context based on the query
            search_results = await self.embedding_service.search_similar(
                query=query_text,
                top_k=5  # Retrieve top 5 most similar content pieces
            )

            if not search_results:
                # No relevant context found
                return {
                    "response": "Information not found in the book content.",
                    "status": "not_found",
                    "citations": []
                }

            # Extract the context from search results
            context_parts = []
            citations = []

            for result in search_results:
                content = result.get("content", "")
                metadata = result.get("metadata", {})
                similarity_score = result.get("similarity_score", 0.0)

                # Only include content with sufficient similarity
                if similarity_score > 0.3:  # Threshold can be adjusted
                    context_parts.append(content)

                    # Add citation information
                    citations.append({
                        "page_path": metadata.get("page_path", ""),
                        "content_snippet": content[:200] + "..." if len(content) > 200 else content,
                        "position": metadata.get("position", 0)
                    })

            if not context_parts:
                # No relevant context found after filtering
                return {
                    "response": "Information not found in the book content.",
                    "status": "not_found",
                    "citations": []
                }

            # Combine all context parts
            context = "\n\n".join(context_parts)

            # Create the prompt with context and query
            messages = self.rag_prompt.format_messages(
                context=context,
                question=query_text
            )

            # Get response from the language model
            response = await self.chat_model.agenerate([messages])

            # Extract the response text
            response_text = response.generations[0][0].text

            # Return the response with status and citations
            return {
                "response": response_text,
                "status": "success",
                "citations": citations
            }

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "response": "An error occurred while processing your query.",
                "status": "error",
                "citations": [],
                "error": str(e)
            }

    async def validate_context_only_response(self, response: str, context: str) -> bool:
        """
        Validate that the response is based only on the provided context
        This is a simplified validation - in practice, you might use more sophisticated methods
        """
        # In a full implementation, this would check if the response contains
        # information that can be verified from the context
        return True  # Placeholder - implement proper validation logic