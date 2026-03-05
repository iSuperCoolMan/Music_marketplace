from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Cookie, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from db.product import get_all_products
from models.products import ProductInCart
from routers.depends import cart_to_dict
from servises.token_handler import get_current_user
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)


@router.get("/", response_class=HTMLResponse)
async def show_main(
        request: Request,
        cart: Annotated[dict[UUID, int], Depends(cart_to_dict)],
        token: str | None = Cookie(default=None)
):
    try:
        user = await get_current_user(token)

        if user.username == "support":
            return await get_support_template(request, token)
        else:
            return await get_main_template(request, cart, token)
    except:
        return await get_main_template(request, cart, token)


async def get_main_template(request: Request, cart: dict[UUID, int], token: str | None):
    db_products = await get_all_products()
    products = []

    for product in db_products:
        product_in_cart = ProductInCart(
            uuid=product.uuid,
            name=product.name,
            price=product.price,
            quantity=product.quantity,
            seller_username=product.seller_username,
            seller_uuid=product.seller_uuid
        )

        if cart:
            if product.uuid in cart.keys():
                product_in_cart.quantity_in_cart = cart[product_in_cart.uuid]
                product_in_cart.total_price = product.price * product_in_cart.quantity_in_cart

        products.append(product_in_cart)

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "products": products,
            "token": token
        }
    )


async def get_support_template(request: Request, token: str | None):
    return templates.TemplateResponse(
        "support_page.html",
        {
            "request": request,
            "token": token
        }
    )


@router.post("/add_to_cart")
async def add_to_cart(
        product_uuid: Annotated[UUID, Depends(UUID)],
        cart: Annotated[dict[UUID, int], Depends(cart_to_dict)]
):
    cart[product_uuid] = 1

    response = RedirectResponse('/', status_code=303)
    response.set_cookie(key="cart", value=str(cart), max_age=3600)
    return response

