from typing import List, Optional

from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel

app = FastAPI()


books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher": "Scribner",
        "publish_date": "1925-04-10",
        "no_of_pages": 180,
        "language": "English",
        "edition": "1st",
        "price": 10.99,
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publisher": "J.B. Lippincott & Co.",
        "publish_date": "1960-07-11",
        "no_of_pages": 281,
        "language": "English",
        "edition": "1st",
        "price": 14.99,
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "publisher": "Secker & Warburg",
        "publish_date": "1949-06-08",
        "no_of_pages": 328,
        "language": "English",
        "edition": "1st",
        "price": 13.99,
    },
    {
        "id": 4,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "publisher": "T. Egerton",
        "publish_date": "1813-01-28",
        "no_of_pages": 279,
        "language": "English",
        "edition": "1st",
        "price": 9.99,
    },
    {
        "id": 5,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "publisher": "Little, Brown and Company",
        "publish_date": "1951-07-16",
        "no_of_pages": 214,
        "language": "English",
        "edition": "1st",
        "price": 12.99,
    },
    {
        "id": 6,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "publisher": "George Allen & Unwin",
        "publish_date": "1937-09-21",
        "no_of_pages": 310,
        "language": "English",
        "edition": "1st",
        "price": 16.99,
    },
    {
        "id": 7,
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "publisher": "George Allen & Unwin",
        "publish_date": "1954-07-29",
        "no_of_pages": 1178,
        "language": "English",
        "edition": "1st",
        "price": 25.99,
    },
    {
        "id": 8,
        "title": "Moby-Dick",
        "author": "Herman Melville",
        "publisher": "Harper & Brothers",
        "publish_date": "1851-10-18",
        "no_of_pages": 635,
        "language": "English",
        "edition": "1st",
        "price": 11.99,
    },
    {
        "id": 9,
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "publisher": "Chatto & Windus",
        "publish_date": "1932-01-01",
        "no_of_pages": 288,
        "language": "English",
        "edition": "1st",
        "price": 13.50,
    },
    {
        "id": 10,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "publisher": "HarperOne",
        "publish_date": "1988-01-01",
        "no_of_pages": 208,
        "language": "English",
        "edition": "1st",
        "price": 12.99,
    },
    {
        "id": 11,
        "title": "The Da Vinci Code",
        "author": "Dan Brown",
        "publisher": "Doubleday",
        "publish_date": "2003-03-18",
        "no_of_pages": 454,
        "language": "English",
        "edition": "1st",
        "price": 17.99,
    },
    {
        "id": 12,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "publisher": "Bloomsbury",
        "publish_date": "1997-06-26",
        "no_of_pages": 223,
        "language": "English",
        "edition": "1st",
        "price": 18.99,
    },
    {
        "id": 13,
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "publisher": "Scholastic Press",
        "publish_date": "2008-09-14",
        "no_of_pages": 374,
        "language": "English",
        "edition": "1st",
        "price": 14.99,
    },
    {
        "id": 14,
        "title": "The Kite Runner",
        "author": "Khaled Hosseini",
        "publisher": "Riverhead Books",
        "publish_date": "2003-05-29",
        "no_of_pages": 371,
        "language": "English",
        "edition": "1st",
        "price": 15.99,
    },
    {
        "id": 15,
        "title": "A Thousand Splendid Suns",
        "author": "Khaled Hosseini",
        "publisher": "Riverhead Books",
        "publish_date": "2007-05-22",
        "no_of_pages": 372,
        "language": "English",
        "edition": "1st",
        "price": 16.00,
    },
]


@app.get("/")
async def home():
    return {"message": "Welcome to FastApi world!"}


# path parameter => name is path parameter
@app.get("/greet/{name}")
async def greet_name(name: str) -> dict:
    return {"message": f"Hello, {name}"}


# query parameter => loc is query parameter
@app.get("/meet-and-greet/")
async def meet_and_greet(loc: str) -> dict:
    return {"message": f"Hello, let's meet at location {loc}"}


# path parameter and query parameter together with default and optional value
@app.get("/greetings/{name}")
async def greetings(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello, {name}. You are {age}'s old"}


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {"title": book_data.title, "author": book_data.author}


@app.get("get_headers")
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agents: str = Header(None),
    host: str = Header(None),
):
    request_header = {}

    request_header["Accept"] = accept
    request_header["Content-type"] = content_type
    request_header["user_agents"] = user_agents
    request_header[host] = host

    return request_header


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


@app.get("/books", status_code=status.HTTP_200_OK, response_model=List[Book])
async def get_books() -> list:
    return books


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK, response_model=Book)
async def get_book(book_id: int) -> dict:
    # filter and map not returns list, we need to make them list
    book = list(filter(lambda book: book["id"] == book_id, books))
    if len(book):
        return book[0]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    # for book in books:
    #     if book["id"] == book_id:
    #         return book
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data: Book) -> dict:
    # model_dump => will create book_data input into a dict which can be inserted into the books list
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@app.patch("/books/{book_id}", status_code=status.HTTP_200_OK, response_model=Book)
async def update_book(book_id: int, book_data: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_data.title
            book["author"] = book_data.author
            book["publisher"] = book_data.publisher
            book["no_of_pages"] = book_data.no_of_pages
            book["langulage"] = book_data.language
            book["price"] = book_data.price
            book["edition"] = book_data.edition
            return book

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
