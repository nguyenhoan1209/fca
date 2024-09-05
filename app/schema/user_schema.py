from typing import List, Optional

from pydantic import BaseModel

from app.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions


class BaseUser(BaseModel):
    email: str
    name: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class BaseUserWithPassword(BaseUser):
    password: str


class User(ModelBaseInfo, BaseUser): 
    ...
    
    class Config:
        from_attributes=True



class FindUser(FindBase, BaseUser, ):
    email__eq: str
    ...


class UpsertUser(BaseUser, ): ...


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
