from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.commentaries import crud
from api_v1.commentaries.schemas import (
    Commentary,
    CommentaryCreate,
)

router = APIRouter(prefix="/api/commentaries", tags=["commentaries"])


@router.post(
    "/",
    response_model=Commentary,
    status_code=status.HTTP_201_CREATED,
)
async def create_commentary(
    comment: CommentaryCreate,
    post_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_commentary(
        session=session, comment_to_create=comment, post_id=post_id
    )
