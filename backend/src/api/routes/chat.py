from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from services.rag_service import RAGService
from models.query import QueryCreate
from config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import time

router = APIRouter()
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
    scope: str = Field(default="full_book", pattern=r"^(full_book|section|page)$")
    section: str = Field(default=None)


class ChatResponse(BaseModel):
    response: str
    status: str = Field(..., pattern=r"^(success|not_found|error)$")
    citations: List[Dict[str, Any]]
    processing_time_ms: int


@router.post("/chat", response_model=Dict[str, Any])
async def chat_endpoint(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Endpoint to handle chat queries and return RAG-based responses
    """
    start_time = time.time()

    try:
        # Initialize RAG service
        rag_service = RAGService()

        # Process the query using RAG
        result = await rag_service.process_query(
            query_text=request.query,
            scope=request.scope,
            section=request.section
        )

        processing_time = round((time.time() - start_time) * 1000, 2)

        # Format the response
        response_data = {
            "response": result.get("response", ""),
            "status": result.get("status", "error"),
            "citations": result.get("citations", []),
            "processing_time_ms": processing_time
        }

        return {
            "status": "success",
            "data": response_data,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

    except HTTPException:
        raise
    except Exception as e:
        processing_time = round((time.time() - start_time) * 1000, 2)
        logger.error(f"Error processing chat query: {str(e)}")
        return {
            "status": "error",
            "error": {
                "code": "PROCESSING_ERROR",
                "message": "Error processing query",
                "details": str(e)
            },
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "processing_time_ms": processing_time
        }