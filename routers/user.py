from fastapi import APIRouter, Cookie
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from db.product import get_products_by_user, create_product
from servises.token_handler import get_current_user
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)


@router.get("/user", response_class=HTMLResponse)
async def user_page(request: Request, token: str | None = Cookie(default=None)):
    user = await get_current_user(token)

    return templates.TemplateResponse(
        "user.html",
        {
            "request": request,
            "token": token,
            "products": await get_products_by_user(user_uuid=user.uuid)
        }
    )


@router.post("/post_product")
async def user_page(request: Request):
    form = await request.form()

    name = form.get("name")
    price = form.get("price")
    quantity = form.get("quantity")

    seller_token = form.get("token")
    seller = await get_current_user(seller_token)

    await create_product(name=name, price=price, quantity=quantity, seller_uuid=seller.uuid)

    return RedirectResponse("/user", status_code=303)