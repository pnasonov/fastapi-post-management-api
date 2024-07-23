from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from core.config import settings

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl=settings.api_v1_prefix + "/auth/token"
)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(
            token,
            key=settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if not username and user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
