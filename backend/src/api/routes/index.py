from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from pydantic import BaseModel, Field
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from services.content_index_service import ContentIndexService
from models.book_content import BookContentCreate
from config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import time
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)


class IndexRequest(BaseModel):
    content: str = Field(..., min_length=10)
    title: str = Field(..., min_length=1, max_length=200)
    page_path: str = Field(..., regex=r'^\/[a-zA-Z0-9\/\-_]*$')
    section: str = Field(default=None)


class IndexResponse(BaseModel):
    indexed_id: str
    message: str
    processing_time_ms: int


@router.post("/index", response_model=Dict[str, Any])
async def index_content_endpoint(
    request: IndexRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Endpoint to index book content into the vector database
    """
    start_time = time.time()

    try:
        # Generate a unique ID for this content
        content_id = str(uuid.uuid4())

        # Create a BookContent object
        from models.book_content import BookContent
        book_content = BookContent(
            id=content_id,
            title=request.title,
            content=request.content,
            section=request.section,
            page_path=request.page_path
        )

        # Initialize content index service
        index_service = ContentIndexService()

        # Index the content
        success = await index_service.index_content(book_content)

        processing_time = round((time.time() - start_time) * 1000, 2)

        if success:
            return {
                "status": "success",
                "data": {
                    "indexed_id": content_id,
                    "message": "Content indexed successfully",
                    "processing_time_ms": processing_time
                },
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to index content")

    except HTTPException:
        raise
    except Exception as e:
        processing_time = round((time.time() - start_time) * 1000, 2)
        logger.error(f"Error indexing content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error indexing content: {str(e)}"
        )


class ListContentResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    limit: int
    offset: int


@router.get("/content", response_model=Dict[str, Any])
async def list_content_endpoint(
    section: str = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Endpoint to retrieve list of available book content
    """
    try:
        # This would normally query the database for content
        # For now, return an empty list as placeholder
        content_list = []
        total = 0

        return {
            "status": "success",
            "data": {
                "items": content_list,
                "total": total,
                "limit": limit,
                "offset": offset
            },
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

    except Exception as e:
        logger.error(f"Error listing content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing content: {str(e)}"
        )