from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Commentary
from api_v1.commentaries.schemas import CommentaryCreate


async def create_commentary(
    session: AsyncSession,
    comment_to_create: CommentaryCreate,
    post_id: int,
) -> Commentary:
    comment_db = Commentary(post_id=post_id, **comment_to_create.model_dump())
    session.add(comment_db)
    await session.commit()
    await session.refresh(comment_db)
    return comment_db


async def get_commentary(
    session: AsyncSession, commentary_id: int
) -> Commentary | None:
    return await session.get(Commentary, commentary_id)


async def delete_commentary(
    session: AsyncSession,
    commentary_db: Commentary,
) -> None:
    await session.delete(commentary_db)
    await session.commit()
    return
