from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import jwt

from core.config import settings

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    username: str, user_id: int, expires_delta: timedelta = timedelta(hours=1)
):
    encode = {
        "sub": username,
        "id": user_id,
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(
        claims=encode,
        key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
