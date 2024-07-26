from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.posts import crud
from api_v1.posts.schemas import PostCreate
from core.models import db_helper


async def get_post_by_id(
    post_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if post := await crud.get_post(session=session, post_id=post_id):
        return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found",
    )


async def check_time_if_autoresponse(post: PostCreate):
    if (
        not post.is_auto_response and not post.response_threshold_in_seconds
    ) or (post.is_auto_response and post.response_threshold_in_seconds):
        return post

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Fix autoresponse settings logic",
    )
