from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.schemas import CreateUserModel, UserLoginModel, UserModel
from src.auth.service import UserService
from src.db.main import get_session

auth_routes = APIRouter()
user_service = UserService()


@auth_routes.post("/singup", response_model=UserModel)
async def create_user(
    user_data: CreateUserModel, session: AsyncSession = Depends(get_session)
):
    user = await user_service.is_user_exits(user_data.email, session)

    if not user:
        new_user = await user_service.create_user(user_data, session)
        return new_user
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email already exits.",
        )


@auth_routes.post("/login", response_model=UserModel)
async def login(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    return await user_service.user_login(user_data, session)


@auth_routes.get("/users", response_model=List[UserModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_users(session)
    return users
