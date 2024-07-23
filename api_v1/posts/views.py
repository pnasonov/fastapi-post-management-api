from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.posts import crud
from api_v1.posts.schemas import (
    Post,
    PostCreate,
    PostUpdate,
    PostUpdatePartial,
    PostDetail,
)
from api_v1.posts import dependencies
from api_v1.auth.dependencies import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[Post])
async def list_posts(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_posts(session=session)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_post(
        session=session, post_to_create=post, user_id=user_id
    )


@router.get("/{post_id}", response_model=PostDetail)
async def get_post_with_commentaries(
    post: Post = Depends(dependencies.get_post_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Post:
    return await crud.get_post_with_comments(session=session, post_db=post)


@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_update: PostUpdate,
    post: Post = Depends(dependencies.get_post_by_id),
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if post.user_id == user_id:
        return await crud.update_post(
            session=session, post_db=post, post_update=post_update
        )

    return HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.patch("/{post_id}", response_model=Post)
async def update_post_partial(
    post_update: PostUpdatePartial,
    post: Post = Depends(dependencies.get_post_by_id),
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if post.user_id == user_id:
        return await crud.update_post(
            session=session,
            post_db=post,
            post_update=post_update,
            partial=True,
        )

    return HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: Post = Depends(dependencies.get_post_by_id),
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if post.user_id == user_id:
        return await crud.delete_post(session=session, post_db=post)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="It is not your post"
    )
