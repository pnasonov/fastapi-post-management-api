from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Post
from api_v1.posts.schemas import (
    PostCreate,
    PostUpdate,
    PostUpdatePartial,
)


async def get_posts(session: AsyncSession) -> list[Post]:
    query = select(Post).order_by(Post.id)
    result: Result = await session.execute(query)
    posts = result.scalars().all()
    return list(posts)


async def get_post(session: AsyncSession, post_id: int) -> Post | None:
    return await session.get(Post, post_id)


async def get_post_with_comments(session: AsyncSession, post_db: Post) -> Post:
    query = (
        select(Post)
        .where(Post.id == post_db.id)
        .options(selectinload(Post.commentaries))
    )
    result: Result = await session.execute(query)
    post = result.scalar()
    return post


async def create_post(
    session: AsyncSession, post_to_create: PostCreate, user_id: int
) -> Post:
    post_db = Post(**post_to_create.model_dump())
    post_db.user_id = user_id
    session.add(post_db)
    await session.commit()
    await session.refresh(post_db)
    return post_db


async def update_post(
    session: AsyncSession,
    post_db: Post,
    post_update: PostUpdate | PostUpdatePartial,
    partial: bool = False,
) -> Post:
    for name, value in post_update.model_dump(exclude_unset=partial).items():
        setattr(post_db, name, value)
    await session.commit()
    return post_db


async def delete_post(
    session: AsyncSession,
    post_db: Post,
) -> None:
    await session.delete(post_db)
    await session.commit()
