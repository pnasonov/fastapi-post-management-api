import asyncio
import datetime

from google import genai
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.posts.schemas import Post
from api_v1.commentaries.crud import create_commentary
from api_v1.commentaries.schemas import CommentaryCreate
from api_v1.vertexai.question_bases import CHECK_IS_OFFENSIVE_TRUE_FALSE

from core.config import settings, scheduler

ai_client = genai.Client(api_key=settings.gemini_api_key)


async def check_is_text_offensive(*args: str) -> bool:
    question = CHECK_IS_OFFENSIVE_TRUE_FALSE + " ".join(args)

    async def ask_model(model: str) -> bool:
        response = await ai_client.aio.models.generate_content(
            model=model,
            contents=question,
        )
        value = response.text.split()[0]
        if value in ("True", "False"):
            return value == "True"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot analise your text",
        )

    try:
        # first, second = await asyncio.gather(
        #     ask_model("gemini-2.5-flash-lite"),
        #     ask_model("gemini-2.0-flash"),
        # )
        first = await ask_model("gemini-2.0-flash")
        second = await ask_model("gemini-2.5-flash-lite")
        if first == second:
            return first

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Text requires human review: inconsistent AI moderation "
                "responses."
            ),
        )
    except (ValueError, IndexError):
        return True


async def generate_response_for_post_and_comment(
        post: str, commentary: str
) -> str:
    question = (
        f"Answer relevant for post: ({post}) and commentary: ({commentary})"
    )
    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question,
    )
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
