from fastapi import APIRouter, Depends
from src.db.models import User
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.schemas import ReviewCreateModel
from .services import ReviewService
from src.auth.dependencies import get_current_user

review_routes = APIRouter()
review_service = ReviewService()


@review_routes.post("/book/{book_uid}")
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await review_service.add_review_to_book(
        book_uid=book_uid,
        review_data=review_data,
        user_email=current_user.email,
        session=session,
    )
