from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..config.database import Base
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ResponseCitationDB(Base):
    __tablename__ = "response_citations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    response_id = Column(String, ForeignKey("query_responses.id"), nullable=False)
    content_id = Column(String, ForeignKey("book_content.id"), nullable=False)
    page_path = Column(String, nullable=False)
    content_snippet = Column(Text, nullable=False)
    position = Column(Integer, nullable=False)  # Position in original content


class ResponseCitation(BaseModel):
    id: Optional[str] = None
    response_id: str
    content_id: str
    page_path: str
    content_snippet: str = Field(..., min_length=1)
    position: int

    class Config:
        from_attributes = True


class ResponseCitationCreate(BaseModel):
    response_id: str
    content_id: str
    page_path: str
    content_snippet: str = Field(..., min_length=1)
    position: int

    class Config:
        from_attributes = True