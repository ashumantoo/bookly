from datetime import datetime
import uuid

from pydantic import BaseModel
from sqlmodel import Field


class CreateUserModel(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: str = Field(min_length=6, max_length=32)
    first_name: str
    last_name: str
    password: str = Field(min_length=6)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserLoginModel(BaseModel):
    email: str
    password: str
