from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..config.database import Base
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class QueryDB(Base):
    __tablename__ = "queries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_text = Column(Text, nullable=False)
    user_id = Column(String, nullable=True)  # Optional, for tracking
    scope = Column(String, nullable=False, default="full_book")  # enum: "full_book", "section", "page"
    section_id = Column(String, nullable=True)  # Optional, if scope is "section"
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QueryModel(BaseModel):
    id: Optional[str] = None
    query_text: str = Field(..., min_length=3, max_length=1000)
    user_id: Optional[str] = None
    scope: str = Field(default="full_book", pattern=r"^(full_book|section|page)$")
    section_id: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class QueryCreate(BaseModel):
    query_text: str = Field(..., min_length=3, max_length=1000)
    user_id: Optional[str] = None
    scope: str = Field(default="full_book", pattern=r"^(full_book|section|page)$")
    section: Optional[str] = None  # This will be converted to section_id in the service

    class Config:
        from_attributes = True