from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.commentaries import crud
from core.models import db_helper


async def get_comment_by_id(
    commentary_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if commentary_db := await crud.get_commentary(
        session=session, commentary_id=commentary_id
    ):
        return commentary_db

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Commentary not found",
    )
