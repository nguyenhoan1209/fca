from contextlib import AbstractAsyncContextManager
from typing import Any, Callable, Type, TypeVar

from sqlalchemy import select, update, delete

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import configs
from app.core.exceptions import DuplicatedError, NotFoundError
from app.model.base_model import BaseModel
from app.util.query_builder import dict_to_sqlalchemy_filter_options

T = TypeVar("T", bound=BaseModel)


class  BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]], model: Type[T]) -> None:
        self.session_factory = session_factory
        self.model = model

    async def read(self):
        async with self.session_factory() as session:
            statement = select(self.model)
            results = await session.scalars(statement)
            return list(results)
            

    async def read_by_id(self, id: int):
        async with self.session_factory() as session:
            statement = select(self.model).where(self.model.id == id)
            result = await session.scalar(statement)
            if not result:
                raise NotFoundError(detail=f"not found id : {id}")
            return result

    async def create(self, schema: T):
        async with self.session_factory() as session:
            new_instance = self.model(**schema.model_dump())
            try:
                session.add(new_instance)
                await session.commit()
                await session.refresh(new_instance)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return new_instance

    async def update(self, id: int, schema: T):
        async with self.session_factory() as session:
            updated_instance = await self.read_by_id(id)
            statement = update(self.model).where(self.model.id == id).values(**schema.model_dump())
            await session.execute(statement)
            await session.commit()
            await session.refresh(updated_instance)
            return self.read_by_id(id)

    async def delete_by_id(self, id: int):
        async with self.session_factory() as session:
            deleted_intance = await self.read_by_id(id)
            statement = delete(self.model).where(self.model.id == id)
            await session.execute(statement)
            await session.commit()
            


    async def close_scoped_session(self):
        return await self.session_factory.close()
