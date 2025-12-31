from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..config.database import Base
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class QueryResponseDB(Base):
    __tablename__ = "query_responses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_id = Column(String, ForeignKey("queries.id"), nullable=False)
    response_text = Column(Text, nullable=False)
    citations = Column(String, nullable=False)  # JSON string
    status = Column(String, nullable=False)  # enum: "success", "not_found", "error"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processing_time_ms = Column(Integer, nullable=True)


class QueryResponse(BaseModel):
    id: Optional[str] = None
    query_id: str
    response_text: str
    citations: List[dict]  # List of citation objects
    status: str = Field(..., regex=r"^(success|not_found|error)$")
    created_at: Optional[datetime] = None
    processing_time_ms: Optional[int] = None

    class Config:
        from_attributes = True


class QueryResponseCreate(BaseModel):
    query_id: str
    response_text: str
    citations: List[dict]
    status: str = Field(..., regex=r"^(success|not_found|error)$")
    processing_time_ms: Optional[int] = None

    class Config:
        from_attributes = True


class QueryResponseUpdate(BaseModel):
    response_text: Optional[str] = None
    citations: Optional[List[dict]] = None
    status: Optional[str] = Field(None, regex=r"^(success|not_found|error)$")
    processing_time_ms: Optional[int] = None

    class Config:
        from_attributes = True