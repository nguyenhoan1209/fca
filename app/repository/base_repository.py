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

    async def read(self, schema: T) -> dict:
        async with self.session_factory() as session:
            schema_as_dict: dict = schema.model_dump(exclude_none=True)
            ordering: str = schema_as_dict.get("ordering", configs.ORDERING)
            order_query = (
                getattr(self.model, ordering[1:]).desc()
                if ordering.startswith("-")
                else getattr(self.model, ordering).asc()
            )
            page = schema_as_dict.get("page", configs.PAGE)
            page_size = schema_as_dict.get("page_size", configs.PAGE_SIZE)
            filter_options = dict_to_sqlalchemy_filter_options(self.model, schema.dict(exclude_none=True))
            query = session.query(self.model)
            filtered_query = query.filter(filter_options)
            query = filtered_query.order_by(order_query)
            if page_size == "all":
                query = query.all()
            else:
                query = query.limit(page_size).offset((page - 1) * page_size).all()
            total_count = filtered_query.count()
            return {
                "founds": query,
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "ordering": ordering,
                    "total_count": total_count,
                },
            }

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
