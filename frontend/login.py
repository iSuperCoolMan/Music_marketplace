from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from frontend.requests_to_api import *
from frontend.cookies import change_user_token

import frontend.cookies


router = APIRouter()

templates = Jinja2Templates(directory="frontend/html")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "token": frontend.cookies.user["token"]
        }
    )


@router.post("/login")
async def post_user(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    response = await try_login(username, password)

    if response:
        change_user_token(response["access_token"])
        return RedirectResponse('/', status_code=303)
    else:
        return RedirectResponse('/login', status_code=303)


@router.get("/exit")
async def post_user(request: Request):
    change_user_token("")
    return RedirectResponse('/', status_code=303)