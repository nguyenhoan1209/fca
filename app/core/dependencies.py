from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import SecurityScopes
from jose import jwt
from pydantic import ValidationError

from app.core.config import configs
from app.core.container import Container
from app.core.exceptions import AuthError, PermissionError
from app.core.security import ALGORITHM, JWTBearer
from app.model.user import User
from app.schema.auth_schema import Payload
from app.services.user_service import UserService


@inject
async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    if security_scopes.scopes and not token_data.scopes:
        raise PermissionError(detail="Not enough permissions")
    if security_scopes.scopes and token_data.scopes not in security_scopes.scopes:
        raise PermissionError(detail="Not enough permissions")
    current_user: User = await service.get_by_id(token_data.id)
    if not current_user:
        raise AuthError(detail="User not found")
    
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


def get_current_user_with_no_exception(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        return None
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        return None
    return current_user


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    if not current_user.is_superuser:
        raise AuthError("It's not a super user")
    return current_user
