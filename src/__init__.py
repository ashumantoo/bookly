from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_routes
from src.errors.auth_errors import register_auth_errors
from src.errors.base_error import register_global_errors
from src.errors.books_errors import register_books_errors
from src.reviews.routes import review_routes
from src.db.redis import redis_client
from contextlib import asynccontextmanager

from src.db.main import init_db


# Below code will run till the time server is live/running
# Database connection will happen here only
@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting....")
    await init_db()
    yield
    await redis_client.close()
    print("Server has been stopped.")


version = "v1"

app = FastAPI(
    version=version,
    title="Bookly",
    description="A REST api for book review web application",
    # lifespan=life_span, #this was getting used when alembic was not implemented, now alembic will handle the database related operations like table creation etc
)

register_auth_errors(app)
register_books_errors(app)
register_global_errors(app)

app.include_router(auth_routes, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(review_routes, prefix=f"/api/{version}/reviews", tags=["Reviews"])
