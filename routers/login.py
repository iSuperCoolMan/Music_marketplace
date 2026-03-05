from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status, Cookie, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from db.user import get_user
from servises.token_handler import Token, link_username_to_token, revoke_access_token
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)

password_hash = PasswordHash.recommended()


async def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await get_user(username=username, with_password=True)
    print(user)

    if not user:
        return False
    if not password_hash.verify(password, user.hashed_password):
        return False

    return user


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, token: Annotated[str | None, Cookie()] = None):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "token": token
        }
    )


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = Token(access_token=link_username_to_token(form_data.username), token_type="bearer")

    response = RedirectResponse('/', status_code=303)
    response.set_cookie(key="token", value=token.access_token, max_age=1800)
    return response


@router.get("/exit", response_class=HTMLResponse)
async def logout(background_tasks: BackgroundTasks, token: Annotated[str | None, Cookie()] = None):
    response = RedirectResponse('/', status_code=303)
    response.set_cookie(key="token", value="", max_age=0)

    background_tasks.add_task(revoke_access_token, token)

    return response



