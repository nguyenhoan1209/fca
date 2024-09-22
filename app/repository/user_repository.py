from contextlib import AbstractAsyncContextManager
from typing import Any, Callable, Type, TypeVar

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.model.user import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)
        
    async def get_by_email(self, email: str) -> User:
        async with self.session_factory() as session:
            statement = select(self.model).where(self.model.email == email)
            result = await session.scalar(statement)
            if not result:
                raise NotFoundError(detail=f"not found email : {email}")
            return result
