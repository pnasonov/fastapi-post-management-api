from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Post
from api_v1.posts.schemas import PostCreate


async def get_posts(session: AsyncSession) -> list[Post]:
    query = select(Post).order_by(Post.id)
    result: Result = await session.execute(query)
    posts = result.scalars().all()
    return list(posts)


async def get_post(session: AsyncSession, post_id: int) -> Post | None:
    return await session.get(Post, post_id)


async def create_post(session: AsyncSession, post: PostCreate) -> Post | None:
    post_db = Post(**post.model_dump())
    session.add(post_db)
    await session.commit()
    await session.refresh(post_db)
    return post_db
