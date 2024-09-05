from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schema.user_schema import User


class SignIn(BaseModel):
    email: str
    password: str
    
    class Config:
        orm_mode = True


class SignUp(BaseModel):
    email: str
    password: str
    name: str

    class Config:
        orm_mode = True

class Payload(BaseModel):
    id: int
    email: str
    name: str
    scopes: str = None
    is_superuser: bool


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user: User
    
    class Config:
        orm_mode = True
