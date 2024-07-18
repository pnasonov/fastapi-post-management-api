from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.models import Base, db_helper
from users.views import router as users_router
from api_v1 import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(posts_router)
app.include_router(users_router)
