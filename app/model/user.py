from enum import Enum
from sqlmodel import Field
from datetime import datetime
from sqlmodel import Column, DateTime, Field, SQLModel, func, Relationship

from app.model.base_model import BaseModel
from app.core.constant import Role

class User(BaseModel, table=True):
    email: str = Field(unique=True)
    password: str = Field()
    user_token: str = Field(unique=True)

    name: str = Field(default=None, nullable=True)
    role: Role = Field(default=Role.USER)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
