from datetime import timedelta, datetime

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.models import User
from src.auth.schemas import CreateUserModel, UserLoginModel
from src.auth.utils import get_password_hash, verify_password, generate_token
from src.constants import REFRESH_TOKEN_EXPIRY
from src.db.redis import add_jti_to_blocklist


class UserService:
    async def get_user_with_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        user = await session.exec(statement)
        if user:
            return user.first()
        else:
            return None

    async def is_user_exits(self, email: str, session: AsyncSession):
        user = await self.get_user_with_email(email, session)
        return True if user is not None else False

    async def get_users(self, session: AsyncSession):
        statement = select(User).order_by(desc(User.created_at))
        users = await session.exec(statement)
        return users.all()

    async def create_user(self, user_data: CreateUserModel, session: AsyncSession):
        user = await self.is_user_exits(user_data.email, session)

        if not user:
            user_data_dict = user_data.model_dump()
            new_user = User(**user_data_dict)  # unpacking user_data dict
            new_user.password = get_password_hash(user_data_dict["password"])
            new_user.role = "user"
            session.add(new_user)
            await session.commit()
            return new_user
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with email already exits.",
            )

    async def user_login(self, user_data: UserLoginModel, session: AsyncSession):
        email = user_data.email
        password = user_data.password

        user = await self.get_user_with_email(email, session)

        if user is not None:
            password_valid = verify_password(password, user.password)

            if password_valid:
                access_token = generate_token(
                    user_data={
                        "email": email,
                        "user_uid": str(user.uid),
                        "role": user.role,
                    },
                )

                refresh_token = generate_token(
                    user_data={
                        "email": email,
                        "user_uid": str(user.uid),
                        "role": user.role,
                    },
                    refresh=True,
                    expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                )
                return JSONResponse(
                    content={
                        "message": "Login Success",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": {"email": email, "uid": str(user.uid)},
                    }
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email or password is invalid",
            )

    async def get_new_access_token(self, token_details):
        expiry_timestamp = token_details["exp"]
        if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
            new_access_token = generate_token(user_data=token_details["user"])
            return JSONResponse(content={"access_token": new_access_token})

        else:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token",
            )

    """
    Revoke the access token on logout so that it can not be used again.
    Blocking the use of the token and revoke it with a TTL 1hr with redis
    """

    async def revoke_access_token(self, token_details):
        jti = token_details["jti"]
        user = token_details["user"]
        await add_jti_to_blocklist(user["email"], jti)

        return JSONResponse(
            content={"message": "Logged out successfully"},
            status_code=status.HTTP_200_OK,
        )
