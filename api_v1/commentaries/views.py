import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.commentaries import crud
from api_v1.commentaries.schemas import (
    Commentary,
    CommentaryCreate,
    DailyStatistic,
)
from api_v1.commentaries import dependencies
from api_v1.auth.dependencies import get_current_user
from api_v1.vertexai.utils import check_is_text_offensive


router = APIRouter(prefix="/commentaries", tags=["commentaries"])


@router.get("/comments-daily-breakdown", response_model=list[DailyStatistic])
async def get_comments_daily_breakdown(
    date_from: Annotated[datetime.date, Path],
    date_to: Annotated[datetime.date, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_daily_breakdown(
        session=session, date_from=date_from, date_to=date_to
    )


@router.post(
    "/", response_model=Commentary, status_code=status.HTTP_201_CREATED
)
async def create_commentary(
    comment: CommentaryCreate,
    post_id: Annotated[int, Path],
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    is_blocked: bool = await check_is_text_offensive(comment.text)
    response = await crud.create_commentary(
        session=session,
        comment_to_create=comment,
        post_id=post_id,
        user_id=user_id,
        is_blocked=is_blocked,
    )

    if is_blocked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Commentary is offensive",
        )
    return response


@router.get("/{comment_id}", response_model=Commentary)
async def get_commentary(
    commentary: Commentary = Depends(dependencies.get_comment_by_id),
):
    return commentary


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_commentary(
    commentary: Commentary = Depends(dependencies.get_comment_by_id),
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if commentary.user_id == user_id:

        return await crud.delete_commentary(
            session=session,
            commentary_db=commentary,
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="It is not your commentary",
    )
