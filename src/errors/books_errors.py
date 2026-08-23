from fastapi import FastAPI, status

from src.errors.base_error import BooklyException, create_exception_handler


class BookNotFound(BooklyException):
    """Book Not found"""

    pass


def register_books_errors(app: FastAPI):
    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book Not Found",
                "error_code": "book_not_found",
            },
        ),
    )
