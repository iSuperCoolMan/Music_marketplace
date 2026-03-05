import jwt
import asyncio

from datetime import datetime, timezone, timedelta

from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from starlette import status

from db.user import get_user
from models.user import User
from settings import token_settings


denylist = set()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def link_username_to_token(username: str):
    access_token_expires = timedelta(minutes=token_settings.EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_settings.SECRET_KEY, algorithm=token_settings.ALGORITHM)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token in denylist:
        raise credentials_exception

    try:
        print(token)
        payload = jwt.decode(token, token_settings.SECRET_KEY, algorithms=[token_settings.ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def revoke_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, token_settings.SECRET_KEY, algorithms=[token_settings.ALGORITHM])
        expire = payload.get("exp")

        if expire is None:
            raise credentials_exception
    except:
        raise credentials_exception

    delta = expire - datetime.now().timestamp()

    denylist.add(token)
    await asyncio.sleep(delta)
    denylist.remove(token)



