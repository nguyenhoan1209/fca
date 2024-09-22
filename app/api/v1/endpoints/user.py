from typing import List
from dependency_injector.wiring import Provide
from app.core.constant import Role
from fastapi import APIRouter, Depends, Security

from app.core.container import Container
from app.core.dependencies import get_current_user
from app.core.middleware import inject
from app.core.security import JWTBearer
from app.schema.base_schema import Blank
from app.schema.user_schema import FindUser, FindUserResult, UpsertUser, User
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(JWTBearer())])


@router.get("", response_model=List[User])
@inject
async def get_user_list(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Security(get_current_user, scopes=[Role.ADMIN.value]),
):
    return await service.get_list()


@router.get("/{user_id}", response_model=User)
@inject
async def get_user(
    user_id: int,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    return await service.get_by_id(user_id)


@router.post("", response_model=User)
@inject
async def create_user(
    user: UpsertUser,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    return await service.add(user)


@router.patch("/{user_id}", response_model=User)
@inject
def update_user(
    user_id: int,
    user: UpsertUser,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    return service.patch(user_id, user)


@router.delete("/{user_id}", response_model=Blank)
@inject
def delete_user(
    user_id: int,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    return service.remove_by_id(user_id)
