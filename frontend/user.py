from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from frontend.cookies import change_user_token
from frontend.requests_to_api import *

import frontend.cookies


router = APIRouter()

templates = Jinja2Templates(directory="frontend/html")


@router.get("/user", response_class=HTMLResponse)
async def user_page(request: Request):
    return templates.TemplateResponse(
        "user.html",
        {
            "request": request,
            "token": frontend.cookies.user["token"],
            "products": await get_products_by_user_token(frontend.cookies.user["token"])
        }
    )


@router.post("/post_product")
async def user_page(request: Request):
    form = await request.form()
    name = form.get("name")
    seller_token = form.get("token")
    price = form.get("price")
    count = form.get("count")

    response = await try_post_product(name, seller_token, price, count)

    return RedirectResponse("/user", status_code=303)