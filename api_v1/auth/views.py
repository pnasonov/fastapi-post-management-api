from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.auth.schemas import User, CreateUser, Token
from api_v1.auth import crud, utils

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register", response_model=User, status_code=status.HTTP_201_CREATED
)
async def register(
    user_to_register: CreateUser,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    return await crud.register_user(session=session, user=user_to_register)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    user = await crud.authenticate_user(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = utils.create_access_token(user.username, user.id)

    return {"access_token": token, "token_type": "bearer"}
