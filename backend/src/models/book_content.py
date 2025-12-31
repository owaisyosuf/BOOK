from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..config.database import Base
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class BookContentDB(Base):
    __tablename__ = "book_content"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    section = Column(String, nullable=True)
    page_path = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    version = Column(Integer, default=1)


class BookContent(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=10)
    section: Optional[str] = None
    page_path: str = Field(..., regex=r'^\/[a-zA-Z0-9\/\-_]*$')
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: Optional[int] = 1

    class Config:
        from_attributes = True


class BookContentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=10)
    section: Optional[str] = None
    page_path: str = Field(..., regex=r'^\/[a-zA-Z0-9\/\-_]*$')

    class Config:
        from_attributes = True


class BookContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    content: Optional[str] = Field(None, min_length=10)
    section: Optional[str] = None

    class Config:
        from_attributes = True