from dependency_injector.wiring import Provide
from app.services.user_service import UserService
from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm

from app.core.container import Container
from app.core.dependencies import get_current_active_user
from app.core.constant import Role

from app.core.middleware import inject

from app.schema.auth_schema import SignIn, SignInResponse, SignUp
from app.schema.user_schema import User
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in")
@inject
async def sign_in(user_info: SignIn, service: AuthService = Depends(Provide[Container.auth_service])):
    return await service.sign_in(user_info)

@router.post("/sign-up", response_model=User)
@inject
async def sign_up(user_info: SignUp, service: AuthService = Depends(Provide[Container.auth_service])):
    return await service.sign_up(user_info)

@router.get("/me", response_model=User)
@inject
def get_me(current_user: User = Security(get_current_active_user)):
    return current_user


