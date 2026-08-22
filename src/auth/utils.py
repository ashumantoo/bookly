from datetime import datetime, timedelta
import logging
import uuid

from passlib.context import CryptContext
import jwt
from src.config import Config
from src.constants import ACCESS_TOKEN_EXPIRY

context = CryptContext(schemes=["sha512_crypt"])


def get_password_hash(password: str) -> str:
    password_hash = context.hash(password)
    return password_hash


def verify_password(plain_password, hash) -> bool:
    is_valid = context.verify(plain_password, hash)
    return is_valid


def generate_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM, payload=payload
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
