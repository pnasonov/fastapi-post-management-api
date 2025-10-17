import datetime

import pytest
from httpx import AsyncClient
from pydantic import TypeAdapter

from api_v1.tests.conftest import (
    authenticated_client,
)
from api_v1.posts.schemas import Post, PostCreate
from api_v1.commentaries.schemas import CommentaryCreate, Commentary
from api_v1.commentaries.crud import create_commentary
from api_v1.tests.db import test_db


@pytest.mark.parametrize(
    "post_to_create",
    [
        PostCreate(
            title="Good post",
            description="Very nice",
            is_auto_response=False,
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_post_success(
    authenticated_client: AsyncClient, post_to_create: PostCreate
):
    response = await authenticated_client.post(
        "/posts/",
        json={
            "user_id": 1,
            **post_to_create.model_dump(),
        },
    )

    assert response.status_code == 201
    assert TypeAdapter(Post).validate_python(response.json())
    for key, value in post_to_create.model_dump().items():
        assert response.json().get(key) == value


@pytest.mark.parametrize(
    "comments_to_create",
    [
        (
            {"text": "comment 1", "user_id": 1, "is_blocked": False},
            {"text": "comment 2", "user_id": 1, "is_blocked": True},
            {"text": "comment 3", "user_id": 1, "is_blocked": False},
            {"text": "comment 4", "user_id": 1, "is_blocked": True},
            {"text": "comment 5", "user_id": 1, "is_blocked": False},
        )
    ],
)
async def test_get_analytics_for_commentaries(
    authenticated_client: AsyncClient,
    comments_to_create: tuple[dict],
):
    for comment in comments_to_create:
        await create_commentary(
            session=test_db.get_scoped_session(),
            comment_to_create=CommentaryCreate(text=comment["text"]),
            post_id=1,
            user_id=1,
            is_blocked=comment["is_blocked"],
        )
    today = datetime.date.today()
    response = await authenticated_client.get(
        "/commentaries/comments-daily-breakdown",
        params=(
            {
                "date_from": today.strftime("%Y-%m-%d"),
                "date_to": (today + datetime.timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                ),
            }
        ),
    )

    assert response.status_code == 200
