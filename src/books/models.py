from datetime import datetime
import numbers

from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4()
        )
    )
    title: str
    author: str
    publisher: str
    publish_date: str
    no_of_pages: int
    language: str
    edition: str
    price: float
    created_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now))

    # string representaton of the book model
    def __repr__(self):
        return f"<Book {self.title}>"
