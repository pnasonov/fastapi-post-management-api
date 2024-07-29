import datetime

import vertexai
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from vertexai.generative_models import GenerativeModel

from api_v1.posts.schemas import Post
from api_v1.commentaries.crud import create_commentary
from api_v1.commentaries.schemas import CommentaryCreate
from api_v1.vertexai.question_bases import OFFENSIVE_TRUE_FALSE

from core.config import settings, scheduler


vertexai.init(
    project=settings.vertex_project_id,
    location=settings.vertex_location,
)
model = GenerativeModel(settings.vertex_generative_model)


async def check_is_text_offensive(*args: str) -> bool:
    question = OFFENSIVE_TRUE_FALSE + " ".join(args)
    try:
        response = await model.generate_content_async(question)
        value = response.text.split()[0]
        if value in ("True", "False"):
            return value == "True"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot analise your text",
        )

    except ValueError:
        return True


async def generate_response_for_post_and_comment(
    post: str, commentary: str
) -> str:
    question = (
        f"Answer relevant for post: ({post}) and commentary: ({commentary})"
    )
    response = await model.generate_content_async(question)
    return response.text


async def run_auto_answer(
    session: AsyncSession, post: Post, commentary_text: str
):
    response = await generate_response_for_post_and_comment(
        post.description, commentary_text
    )

    @scheduler.scheduled_job(
        "date",
        run_date=datetime.datetime.now()
        + datetime.timedelta(seconds=post.response_threshold_in_seconds),
    )
    async def scheduled_create_commentary() -> None:
        await create_commentary(
            session=session,
            comment_to_create=CommentaryCreate(text=response),
            post_id=post.id,
            user_id=post.user_id,
            is_blocked=False,
        )
