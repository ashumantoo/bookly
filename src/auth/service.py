from datetime import timedelta, datetime

from fastapi import HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.auth.schemas import (
    CreateUserModel,
    PasswordResetConfirmModel,
    PasswordResetRequestModel,
    UserLoginModel,
)
from src.auth.utils import get_password_hash, verify_password, generate_token
from src.constants import REFRESH_TOKEN_EXPIRY
from src.db.redis import add_jti_to_blocklist
from src.errors.auth_errors import (
    InvalidCredentials,
    InvalidToken,
    UserAlreadyExists,
    UserNotFound,
)
from src.mail import create_message, mail
from src.config import Config
from src.auth.utils import create_url_safe_token, decode_url_safe_token


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

    async def create_user(
        self,
        user_data: CreateUserModel,
        bg_tasks: BackgroundTasks,
        session: AsyncSession,
    ):
        user = await self.is_user_exits(user_data.email, session)

        if not user:
            user_data_dict = user_data.model_dump()
            new_user = User(**user_data_dict)  # unpacking user_data dict
            new_user.password = get_password_hash(user_data_dict["password"])
            new_user.role = "user"
            session.add(new_user)
            await session.commit()

            # send email varification email
            email_token = create_url_safe_token({"email": user_data.email})

            link = f"http://{Config.DOMAIN_NAME}/api/v1/auth/verify/{email_token}"

            html_message = f"""
            <h1>Verify your email</h1>
            <p>Please click this <a href="{link}">link</a> to verify your email</p>
            """

            message = create_message(
                recipients=[user_data.email],
                subject="Verify your email",
                body=html_message,
            )

            # await mail.send_message(message)

            # Pushing send email task in the background using inbuilt fastapi BackgroundTasks to unblock the main processor
            # since sending email is taking time to execute. add_task function takes two args 1st: is the function, 2nd is
            # the params required for the function while calling.
            bg_tasks.add_task(mail.send_message, message)

            return {
                "message": "User account created! check email to verify your account",
                "user": new_user,
            }
        else:
            raise UserAlreadyExists()

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
                raise InvalidCredentials()
        else:
            raise InvalidCredentials()

    async def get_new_access_token(self, token_details):
        expiry_timestamp = token_details["exp"]
        if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
            new_access_token = generate_token(user_data=token_details["user"])
            return JSONResponse(content={"access_token": new_access_token})

        else:
            raise InvalidToken()

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

    async def send_email(self, emails: list[str]):
        html = "<h3>Welcom to Bookly app<h3>"

        message = create_message(recipients=emails, subject="Welcome", body=html)

        await mail.send_message(message)

        return {"message": "Email send successfully."}

    async def verify_email(self, email_token: str, session: AsyncSession):
        token_data = decode_url_safe_token(token=email_token)
        user_email = token_data.get("email")

        if user_email:
            user = await self.get_user_with_email(email=user_email, session=session)

            if not user:
                raise UserNotFound()

            await self.update_user(user, {"is_verified": True}, session)

            return JSONResponse(
                content={"message": "Account verified successfully"},
                status_code=status.HTTP_200_OK,
            )

        return JSONResponse(
            content={"message": "Error occured during verification."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    async def update_user(
        self, user: User, updated_user_data: dict, session: AsyncSession
    ):
        for k, v in updated_user_data.items():
            setattr(user, k, v)

        await session.commit()
        return user

    async def password_reset_request(
        self,
        password_reset_data: PasswordResetRequestModel,
        bg_tasks: BackgroundTasks,
        session: AsyncSession,
    ):
        email = password_reset_data.email
        user = await self.get_user_with_email(email, session)
        if not user:
            raise UserNotFound()

        reset_token = create_url_safe_token({"email": email})

        link = f"http://{Config.DOMAIN_NAME}/api/v1/auth/password-reset-confirm/{reset_token}"

        html_message = f"""
        <h1>Reset your password</h1>
        <p>Please click this <a href="{link}">link</a> to reset your password.</p>
        """

        message = create_message(
            recipients=[email],
            subject="Reset your password",
            body=html_message,
        )

        # await mail.send_message(message)
        # Handling through background task
        bg_tasks.add_task(mail.send_message, message)

        return JSONResponse(
            content={
                "message": "Please check your email for instruction to reset your password.",
            },
            status_code=status.HTTP_200_OK,
        )

    async def reset_account_password(
        self, token: str, passwords: PasswordResetConfirmModel, session: AsyncSession
    ):
        if passwords.new_password != passwords.confirm_new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password did not match with confirm new password",
            )
        token_data = decode_url_safe_token(token)
        user_email = token_data.get("email")

        if user_email:
            user = await self.get_user_with_email(email=user_email, session=session)

            if not user:
                raise UserNotFound()

            new_password_hash = get_password_hash(password=passwords.new_password)

            await self.update_user(user, {"password": new_password_hash}, session)

            return JSONResponse(
                content={"message": "Password reset successfully"},
                status_code=status.HTTP_200_OK,
            )

        return JSONResponse(
            content={"message": "Error occured during password reset."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
