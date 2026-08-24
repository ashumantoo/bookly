from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.auth.schemas import (
    CreateUserModel,
    EmailModel,
    PasswordResetConfirmModel,
    PasswordResetRequestModel,
    UserLoginModel,
    UserModel,
    UserBooksModel,
)
from src.auth.service import UserService
from src.db.main import get_session

auth_routes = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


@auth_routes.post("/signup")
async def create_user(
    user_data: CreateUserModel, session: AsyncSession = Depends(get_session)
):
    return await user_service.create_user(user_data, session)


@auth_routes.post("/login", response_model=UserModel)
async def login(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    return await user_service.user_login(user_data, session)


# here user is not a function argument that we need to pass when we call it. instead this user data
# we are receing it from get_current_user function throught the dependancy
@auth_routes.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user: dict = Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_routes.post("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    return await user_service.get_new_access_token(token_details)


@auth_routes.get("/users", response_model=List[UserModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await user_service.get_users(session)


@auth_routes.post("/logout", response_model=UserModel)
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    return await user_service.revoke_access_token(token_details)


@auth_routes.post("/send_mail")
async def send_mail(emails: EmailModel):
    return await user_service.send_email(emails=emails.email_addresses)


@auth_routes.get("/verify/{token}")
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    return await user_service.verify_email(email_token=token, session=session)


@auth_routes.post("/password-reset-request")
async def password_reset_request(
    password_reset_data: PasswordResetRequestModel,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.password_reset_request(password_reset_data, session)


@auth_routes.post("/password-reset-confirm/{token}")
async def password_reset_request(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.reset_account_password(token, passwords, session)
