from fastapi import APIRouter

from api_v1.posts.views import router as posts_router

router = APIRouter()

router.include_router(posts_router)
