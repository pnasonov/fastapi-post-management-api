from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from posts_views import router as posts_router
from users.views import router as users_router

app = FastAPI()
app.include_router(posts_router)
app.include_router(users_router)
