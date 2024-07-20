from contextlib import asynccontextmanager

from fastapi import FastAPI

from users.views import router as users_router
from api_v1 import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(posts_router)
app.include_router(users_router)
