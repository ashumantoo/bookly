from passlib.context import CryptContext

context = CryptContext(schemes=["sha512_crypt"])


def get_password_hash(password: str) -> str:
    password_hash = context.hash(password)
    return password_hash


def verify_password(plain_password, hash) -> bool:
    is_valid = context.verify(plain_password, hash)
    return is_valid
