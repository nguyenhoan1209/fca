from sqlmodel import Field
from datetime import datetime
from sqlmodel import Column, DateTime, Field, SQLModel, func, Relationship
from app.model.base_model import BaseModel
from app.model.user import User


class Post(BaseModel, table=True):
    title: str = Field(default=None, nullable=True)
    content: str = Field(default=None, nullable=True)
    is_published: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)