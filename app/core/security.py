from datetime import datetime, timedelta
from typing import Tuple

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.config import configs
from app.core.exceptions import AuthError, PermissionError
from app.core.constant import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(subject: dict, expires_delta: timedelta = None) -> Tuple[str, str]:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, configs.SECRET_KEY, algorithm=ALGORITHM)
    expiration_datetime = expire.strftime(configs.DATETIME_FORMAT)
    return encoded_jwt, expiration_datetime


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        return (
            decoded_token
            if decoded_token["exp"] >= int(round(datetime.now().timestamp()))
            else None
        )
    except Exception as e:
        return {}


class JWTBearer(OAuth2PasswordBearer):
    def __init__(
        self,
        tokenUrl: str = "api/v1/auth/sign-in",
        scopes={Role.ADMIN.value: "Admin", Role.USER.value: "User"},
        auto_error: bool = True,
    ):
        super(JWTBearer, self).__init__(tokenUrl=tokenUrl, scopes=scopes, auto_error=auto_error)
