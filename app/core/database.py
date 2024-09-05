from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any, AsyncGenerator

from loguru import logger

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


@as_declarative()
class BaseModel:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            logger.info("Creating tables")
            await conn.run_sync(BaseModel.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, AbstractAsyncContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()