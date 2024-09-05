from typing import Any, Protocol


class RepositoryProtocol(Protocol):
    async def read_by_options(self, schema: Any) -> Any: ...

    async def read_by_id(self, id: int) -> Any: ...

    async def create(self, schema: Any) -> Any: ...

    async def update(self, id: int, schema: Any) -> Any: ...

    async def update_attr(self, id: int, attr: str, value: Any) -> Any: ...

    async def whole_update(self, id: int, schema: Any) -> Any: ...

    async def delete_by_id(self, id: int) -> Any: ...


class BaseService:
    def __init__(self, repository: RepositoryProtocol) -> None:
        self._repository = repository

    async def get_list(self, schema: Any) -> Any:
        return self._repository.read_by_options(schema)

    async def get_by_id(self, id: int) -> Any:
        return await self._repository.read_by_id(id)

    async def add(self, schema: Any) -> Any:
        return await self._repository.create(schema)

    async def patch(self, id: int, schema: Any) -> Any:
        return await self._repository.update(id, schema)

    async def patch_attr(self, id: int, attr: str, value: Any) -> Any:
        return await self._repository.update_attr(id, attr, value)

    async def put_update(self, id: int, schema: Any) -> Any:
        return await self._repository.whole_update(id, schema)

    async def remove_by_id(self, id: int) -> Any:
        return await self._repository.delete_by_id(id)

    async def close_scoped_session(self):
        await self._repository.close_scoped_session()
