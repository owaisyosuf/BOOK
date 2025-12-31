import logging
from typing import Dict, Any, Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.book_content import BookContent
from config.database import get_db
from config.settings import settings
from services.embedding_service import EmbeddingService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.book_content import BookContentDB
import uuid

logger = logging.getLogger(__name__)


class ContentIndexService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    async def index_content(self, content: BookContent) -> bool:
        """
        Index a piece of book content by creating embeddings and storing in vector DB
        """
        try:
            # Prepare metadata for the content
            metadata = {
                "id": content.id or str(uuid.uuid4()),
                "title": content.title,
                "section": content.section,
                "page_path": content.page_path,
                "version": content.version or 1
            }

            # Store content in vector database
            success = await self.embedding_service.store_content(
                content_id=metadata["id"],
                text=content.content,
                metadata=metadata
            )

            if success:
                logger.info(f"Successfully indexed content with ID: {metadata['id']}")
            else:
                logger.error(f"Failed to index content with ID: {metadata['id']}")

            return success
        except Exception as e:
            logger.error(f"Error indexing content: {str(e)}")
            return False

    async def update_content_index(self, content: BookContent) -> bool:
        """
        Update an existing content's index
        """
        try:
            # Delete old content first
            if content.id:
                await self.embedding_service.delete_content(content.id)

            # Re-index the content
            return await self.index_content(content)
        except Exception as e:
            logger.error(f"Error updating content index: {str(e)}")
            return False

    async def remove_content_from_index(self, content_id: str) -> bool:
        """
        Remove content from the index
        """
        try:
            success = await self.embedding_service.delete_content(content_id)
            if success:
                logger.info(f"Successfully removed content from index: {content_id}")
            else:
                logger.error(f"Failed to remove content from index: {content_id}")

            return success
        except Exception as e:
            logger.error(f"Error removing content from index: {str(e)}")
            return False

    async def index_all_content(self, db_session: AsyncSession) -> bool:
        """
        Index all existing book content in the database
        """
        try:
            # Get all book content from the database
            result = await db_session.execute(select(BookContentDB))
            all_content = result.scalars().all()

            indexed_count = 0
            for content_db in all_content:
                # Convert DB model to Pydantic model
                content = BookContent(
                    id=content_db.id,
                    title=content_db.title,
                    content=content_db.content,
                    section=content_db.section,
                    page_path=content_db.page_path,
                    created_at=content_db.created_at,
                    updated_at=content_db.updated_at,
                    version=content_db.version
                )

                # Index the content
                if await self.index_content(content):
                    indexed_count += 1

            logger.info(f"Indexed {indexed_count} content items")
            return True
        except Exception as e:
            logger.error(f"Error indexing all content: {str(e)}")
            return False