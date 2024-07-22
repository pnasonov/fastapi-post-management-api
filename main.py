from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from users.views import router as users_router
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
app.include_router(users_router)
