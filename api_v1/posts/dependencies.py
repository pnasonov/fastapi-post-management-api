from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.posts import crud
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
