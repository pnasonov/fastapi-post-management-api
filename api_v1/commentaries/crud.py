from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.commentaries.schemas import CommentaryCreate
from core.models import Commentary


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
