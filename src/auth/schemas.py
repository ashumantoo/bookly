from datetime import datetime
from typing import List
import uuid

from pydantic import BaseModel
from sqlmodel import Field

from src.books.schemas import Book
from src.reviews.schemas import ReviewModel


class CreateUserModel(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: str = Field(min_length=6, max_length=32)
    first_name: str
    last_name: str
    password: str = Field(min_length=6)


from src.books.schemas import Book


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


class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str
    password: str
