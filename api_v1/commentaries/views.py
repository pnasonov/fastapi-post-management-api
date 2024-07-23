from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.commentaries import crud
from api_v1.commentaries.schemas import (
    Commentary,
    CommentaryCreate,
)
from api_v1.commentaries import dependencies
from api_v1.auth.dependencies import get_current_user

router = APIRouter(prefix="/commentaries", tags=["commentaries"])


@router.post(
    "/", response_model=Commentary, status_code=status.HTTP_201_CREATED
)
async def create_commentary(
    comment: CommentaryCreate,
    post_id: Annotated[int, Path],
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_commentary(
        session=session,
        comment_to_create=comment,
        post_id=post_id,
        user_id=user_id,
    )


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

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It is not your commentary")
