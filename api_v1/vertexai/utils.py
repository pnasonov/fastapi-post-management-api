import vertexai
from fastapi import HTTPException, status
from vertexai.generative_models import GenerativeModel

from api_v1.vertexai.question_bases import OFFENSIVE_TRUE_FALSE
from core.config import settings


vertexai.init(
    project=settings.vertex_project_id,
    location=settings.vertex_location,
)

model = vertexai.generative_models.GenerativeModel(settings.generative_model)


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
