from datetime import date, datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy as sa
import uuid


# with sa_column, we are telling python to treat this column as sqlalchemy column instead of sqlModel column
# often we do this if we have to pass some custom meta data to the column
class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    )
    title: str
    category: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = Field(default=None, sa_column=Column(sa.Text))
    author: str
    publisher: str
    publish_date: date
    no_of_pages: int
    language: str
    edition: str
    price: float
    image_url: Optional[str] = Field(default=None)
    # Creating Relation between user and books
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.now
        )
    )

    # string representaton of the book model
    def __repr__(self):
        return f"<Book {self.title}>"
