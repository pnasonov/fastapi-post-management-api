import os
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"


class DBSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = True  # for dev and debug


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DBSettings = DBSettings()
    jwt_secret_key: str = os.environ["JWT_SECRET_KEY"]
    jwt_algorithm: str = os.environ["JWT_ALGORITHM"]
    vertex_project_id: str = os.environ["VERTEX_PROJECT_ID"]
    vertex_location: str = os.environ["VERTEX_LOCATION"]
    vertex_generative_model: str = os.environ["VERTEX_GENERATIVE_MODEL"]


settings = Settings()
scheduler = AsyncIOScheduler()
