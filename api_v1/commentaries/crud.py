import datetime

from pydantic import TypeAdapter
from sqlalchemy import select, Result, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Commentary
from api_v1.commentaries.schemas import (
    CommentaryCreate,
    DailyStatistic,
)


async def create_commentary(
    session: AsyncSession,
    comment_to_create: CommentaryCreate,
    post_id: int,
    user_id: int,
    is_blocked: bool,
) -> Commentary:
    comment_db = Commentary(post_id=post_id, **comment_to_create.model_dump())
    comment_db.user_id = user_id
    comment_db.is_blocked = is_blocked
    session.add(comment_db)
    await session.commit()
    await session.refresh(comment_db)
    return comment_db


async def get_commentary(
    session: AsyncSession, commentary_id: int
) -> Commentary | None:
    query = select(Commentary).where(
        Commentary.id == commentary_id,
        Commentary.is_blocked == False,
    )
    result: Result = await session.execute(query)
    return result.scalar()


async def get_daily_breakdown(
    session: AsyncSession, date_from: datetime.date, date_to: datetime.date
) -> list[DailyStatistic]:
    query = (
        select(
            func.date(Commentary.timestamp).label("date"),
            func.count(Commentary.id).label("comment_count"),
            func.sum(
                case(
                    (Commentary.is_blocked, 1),
                    else_=0,
                )
            ).label("blocked_count"),
        )
        .filter(Commentary.timestamp.between(date_from, date_to))
        .group_by(func.date(Commentary.timestamp))
    )
    result: Result = await session.execute(query)
    rows = result.mappings()
    adapter = TypeAdapter(list[DailyStatistic])
    all_days_stat = adapter.validate_python(rows)
    return all_days_stat


async def delete_commentary(
    session: AsyncSession,
    commentary_db: Commentary,
) -> None:
    await session.delete(commentary_db)
    await session.commit()
    return
