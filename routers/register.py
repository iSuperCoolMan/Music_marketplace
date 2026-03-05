from typing import Annotated

from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from servises.token_handler import Token, link_username_to_token
from db.user import create_user
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)

password_hash = PasswordHash.recommended()


@router.get("/register", response_class=HTMLResponse)
async def show_register(request: Request, token: Annotated[str | None, Cookie()] = None):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "token": token
        }
    )


@router.post("/register")
async def register_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):

    await create_user(
        username=form_data.username,
        hashed_password=password_hash.hash(form_data.password)
    )

    token = Token(access_token=link_username_to_token(form_data.username), token_type="bearer")

    response = RedirectResponse('/', status_code=303)
    response.set_cookie(key="token", value=token.access_token, max_age=1800)
    return response