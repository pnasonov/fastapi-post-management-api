from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.utils import bcrypt_context
from core.models.user import User
from api_v1.auth import schemas


async def register_user(
    session: AsyncSession, user: schemas.CreateUser
) -> User:
    user.password = bcrypt_context.hash(user.password)
    user_db = User(**user.model_dump())
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User | None:
    query = select(User).filter(User.username == username)
    result: Result = await session.execute(query)
    user = result.scalar()

    if user and bcrypt_context.verify(password, user.password):
        return user
