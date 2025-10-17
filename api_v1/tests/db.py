from core.models.database import DatabaseHelper
from core.config import BASE_DIR

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# DATABASE_NAME = BASE_DIR / "test_db.sqlite3"
# DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_NAME}"

test_db = DatabaseHelper(DATABASE_URL)
