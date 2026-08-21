from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))


async def init_db():
    async with engine.begin() as db_connection:
        from src.books.models import Book

        # Create all the database tables
        await db_connection.run_sync(SQLModel.metadata.create_all)
