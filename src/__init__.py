from fastapi import FastAPI
from src.books.router import book_router
from contextlib import asynccontextmanager

from src.db.main import init_db


# Below code will run till the time server is live/running
# Database connection will happen here only
@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting....")
    await init_db()
    yield
    print("Server has been stopped.")


version = "v1"

app = FastAPI(
    version=version,
    title="Bookly",
    description="A REST api for book review web application",
    lifespan=life_span,
)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
