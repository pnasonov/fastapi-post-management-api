import pytest
from fastapi import HTTPException, status
from httpx import AsyncClient
from sqlalchemy import select

from api_v1.tests.conftest import (
    authenticated_client,
)
from api_v1.tests.db import test_db
from core.models import Post as PostModel


@pytest.mark.asyncio
async def test_create_post_offensive_blocked(
        authenticated_client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    async def mock_check_is_text_offensive(*_: str) -> bool:
        return True

    monkeypatch.setattr(
        "api_v1.posts.views.check_is_text_offensive", mock_check_is_text_offensive
    )
    response = await authenticated_client.post(
        "/posts/",
        json={
            "user_id": 1,
            "title": "You are useless",
            "description": "Get lost, nobody wants you here.",
            "is_auto_response": False,
            "response_threshold_in_seconds": 0,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    session = test_db.get_scoped_session()
    result = await session.execute(select(PostModel))
    posts = result.scalars().all()
    assert len(posts) == 1
    assert posts[0].is_blocked is True


@pytest.mark.asyncio
async def test_create_post_not_offensive(
        authenticated_client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    async def mock_check_is_text_offensive(*_: str) -> bool:
        return False

    monkeypatch.setattr(
        "api_v1.posts.views.check_is_text_offensive", mock_check_is_text_offensive
    )
    response = await authenticated_client.post(
        "/posts/",
        json={
            "user_id": 1,
            "title": "Gardening tips",
            "description": "Sharing a few ideas on tomatoes and basil.",
            "is_auto_response": False,
            "response_threshold_in_seconds": 0,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    session = test_db.get_scoped_session()
    result = await session.execute(select(PostModel))
    post_db = result.scalars().one()
    assert post_db.is_blocked is False
    assert post_db.title == "Gardening tips"


@pytest.mark.asyncio
async def test_create_post_needs_human_review(
        authenticated_client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    async def mock_check_is_text_offensive(*_: str) -> bool:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Text requires human review: inconsistent AI moderation responses.",
        )

    monkeypatch.setattr(
        "api_v1.posts.views.check_is_text_offensive", mock_check_is_text_offensive
    )
    response = await authenticated_client.post(
        "/posts/",
        json={
            "user_id": 1,
            "title": "Nice try genius",
            "description": "Sure, you're brilliant... or maybe not.",
            "is_auto_response": False,
            "response_threshold_in_seconds": 0,
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
