from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.posts import crud
from api_v1.posts.schemas import Post, PostCreate

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("/", response_model=list[Post])
async def list_posts(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_posts(session=session)


@router.post("/", response_model=Post)
async def list_posts(
    post: PostCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_post(session=session, post=post)


@router.get("/{post_id}", response_model=Post)
async def list_posts(
    post_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if post := await crud.get_post(session=session, post_id=post_id):
        return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found",
    )
