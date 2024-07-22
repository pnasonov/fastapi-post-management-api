from fastapi import APIRouter

from api_v1.posts.views import router as posts_router
from api_v1.commentaries.views import router as commentaries_router

router = APIRouter()

router.include_router(posts_router)
router.include_router(commentaries_router)
