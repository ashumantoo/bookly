from datetime import date, datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy as sa
import uuid

"""
 => Circular Import Issue
    occurs when two or more modules depend on each other directly or indirectly, causing an infinite loop during 
    the module loading process
    
 - Database models has been moved to single models.py file to resolve the circular import issue which will might
   raise by keeping the database models into sepearate files.
  
"""


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    password: str = Field(
        exclude=True  # exclude=True will exclude this field when the reposne will return to client
    )
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
    # populate books using back_populate relationship provided by sqlmodel
    # selectin : with the help of this sqlmodel loads all the books by using primary key at once.
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


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
    # populate user using back_populate relationship provideby by sqlmodel
    # value to back_populates is not the table name but the property/field on the User sqlmodel Model
    user: Optional[User] = Relationship(back_populates="books")

    # string representaton of the book model
    def __repr__(self):
        return f"<Book {self.title}>"
