from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.models import User
from src.auth.schemas import CreateUserModel
from src.auth.utils import get_password_hash


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
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)  # unpacking user_data dict
        new_user.password = get_password_hash(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        return new_user
