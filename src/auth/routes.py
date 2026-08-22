from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RefreshTokenBearer
from src.auth.schemas import CreateUserModel, UserLoginModel, UserModel
from src.auth.service import UserService
from src.db.main import get_session

auth_routes = APIRouter()
user_service = UserService()


@auth_routes.post("/singup", response_model=UserModel)
async def create_user(
    user_data: CreateUserModel, session: AsyncSession = Depends(get_session)
):
    return await user_service.create_user(user_data, session)


@auth_routes.post("/login", response_model=UserModel)
async def login(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    return await user_service.user_login(user_data, session)


@auth_routes.post("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    return await user_service.get_new_access_token(token_details)


@auth_routes.get("/users", response_model=List[UserModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await user_service.get_users(session)
