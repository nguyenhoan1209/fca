from sqlmodel import Field
from datetime import datetime
from sqlmodel import Column, DateTime, Field, SQLModel, func, Relationship
from app.model.base_model import BaseModel


class Tag(BaseModel, table=True):
    name: str = Field(unique=True)
    description: str = Field(default=None, nullable=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
