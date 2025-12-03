import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from api_v1.tests.db import test_db
from core.models import Base
from core.models.database import db_helper


@pytest.fixture(scope="function")
async def setup_database():

    async with test_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_client(setup_database):
    app.dependency_overrides[db_helper.session_dependency] = (
        test_db.session_dependency
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1/api/v1",
    ) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def authenticated_client(test_client):
    await test_client.post(
        "/auth/register",
        json={"username": "user", "password": "pass"},
    )
    token = await test_client.post(
        "/auth/token",
        data={"username": "user", "password": "pass"},
    )
    test_client.headers.update(
        {"Authorization": f"Bearer {token.json()['access_token']}"}
    )
    return test_client
