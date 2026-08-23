from __future__ import annotations  # 1. Postpones annotation evaluation
from datetime import date, datetime
import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from src.auth.schemas import UserModel

"""
=> Circular Import Issue
    occurs when two or more modules depend on each other directly or indirectly, causing an infinite loop during 
    the module loading process
    
 - Cicular import issue can happen at database model lavel or pydentic schema level also    
   
 - To solve the circular import problem with the large application we can follow some other approaches like keeping
   
    1. Add from __future__ import annotations to the very top of your files.
    
    2. Place the conflicting import inside an if TYPE_CHECKING: block.
    
    3. Reference the linked model directly in your type hints.
    
    4. Call YourModel.model_rebuild() at the bottom of the file to resolve the types. 
    
    
  from __future__ import annotations # 1. Postpones annotation evaluation
  from typing import TYPE_CHECKING, List
  from pydantic import BaseModel

  # 2. Guard the import so it is only seen by type checkers, not runtime Python
  if TYPE_CHECKING:
      from .item import ItemSchema

  class UserSchema(BaseModel):
      id: int
      name: str
      items: List[ItemSchema] = [] # 3. Use the type hint normally

  # 4. Rebuild the model at the very bottom of the file
  from .item import ItemSchema
  UserSchema.model_rebuild()
"""


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


class BookWithUser(Book):
    user: UserModel | None = None


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


from src.auth.schemas import UserModel

BookWithUser.model_rebuild()
