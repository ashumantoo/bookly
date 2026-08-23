from datetime import date, datetime
import uuid

from pydantic import BaseModel


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    category: str
    description: str
    author: str
    publisher: str
    publish_date: date
    no_of_pages: int
    language: str
    edition: str
    price: float
    image_url: str
    created_at: datetime
    updated_at: datetime


class BookCreateModel(BaseModel):
    title: str
    category: str
    description: str
    author: str
    publisher: str
    no_of_pages: int
    publish_date: date
    language: str
    edition: str
    price: float
    image_url: str


class BookUpdateModel(BaseModel):
    title: str
    category: str
    description: str
    author: str
    publisher: str
    no_of_pages: int
    language: str
    edition: str
    price: float
    image_url: str
