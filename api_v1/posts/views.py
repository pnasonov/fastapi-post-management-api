from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.posts import crud
from api_v1.posts.schemas import Post, PostCreate, PostUpdate
from api_v1.posts import dependencies

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("/", response_model=list[Post])
async def list_posts(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_posts(session=session)


@router.post("/", response_model=Post)
async def create_post(
    post: PostCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_post(session=session, post_to_create=post)


@router.get("/{post_id}", response_model=Post)
async def get_post(
    post: Post = Depends(dependencies.get_post_by_id),
) -> Post:
    return post


@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_update: PostUpdate,
    post: Post = Depends(dependencies.get_post_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_post(
        session=session, post_db=post, post_update=post_update
    )
