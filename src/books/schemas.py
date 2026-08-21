from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    publish_date: str
    no_of_pages: int
    language: str
    edition: str
    price: float


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    no_of_pages: int
    language: str
    edition: str
    price: float
