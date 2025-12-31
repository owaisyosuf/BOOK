from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from ..config.database import Base
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class RetrievedContextDB(Base):
    __tablename__ = "retrieved_context"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_id = Column(String, ForeignKey("queries.id"), nullable=False)
    content_id = Column(String, ForeignKey("book_content.id"), nullable=False)
    content_snippet = Column(Text, nullable=False)
    similarity_score = Column(Float, nullable=False)  # 0.0 to 1.0
    page_path = Column(String, nullable=False)
    position = Column(Integer, nullable=False)  # Position in original content


class RetrievedContext(BaseModel):
    id: Optional[str] = None
    query_id: str
    content_id: str
    content_snippet: str = Field(..., min_length=1)
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    page_path: str
    position: int

    class Config:
        from_attributes = True


class RetrievedContextCreate(BaseModel):
    query_id: str
    content_id: str
    content_snippet: str = Field(..., min_length=1)
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    page_path: str
    position: int

    class Config:
        from_attributes = True