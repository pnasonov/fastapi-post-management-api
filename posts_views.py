from fastapi import APIRouter

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("/")
def list_posts():
    return "Works!"
