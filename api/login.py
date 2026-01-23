from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel
from api.database import *
from api.token_handler import Token, link_username_to_token


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


password_hash = PasswordHash.recommended()

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user = get_user(username)

    if not user:
        return False
    if not password_hash.verify(password, user["hashed_password"]):
        return False

    return user


@router.post("/api/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = link_username_to_token(user["username"])

    return Token(access_token=access_token, token_type="bearer")


@router.post("/api/register")
async def register_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    create_user(
        form_data.username,
        password_hash.hash(form_data.password)
    )

    access_token = link_username_to_token(form_data.username)

    return Token(access_token=access_token, token_type="bearer")