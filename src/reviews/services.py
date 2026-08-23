from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService

from fastapi import HTTPException, status
import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from src.errors.auth_errors import UserNotFound
from src.errors.books_errors import BookNotFound

from .schemas import ReviewCreateModel

book_service = BookService()
user_service = UserService()


class ReviewService:
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            book = await book_service.get_book(book_uid, session)

            user = await user_service.get_user_with_email(
                email=user_email, session=session
            )

            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)

            if not book:
                raise BookNotFound

            if not user:
                raise UserNotFound()

            new_review.user = user
            new_review.book = book

            session.add(new_review)
            await session.commit()
            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong",
            )
