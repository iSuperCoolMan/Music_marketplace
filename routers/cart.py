from typing import Annotated

from uuid import UUID
from fastapi import APIRouter, Cookie
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from db.product import get_products_by_uuids
from models.products import ProductInCart
from routers.depends import cart_to_dict
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)

cart_amount = 0


@router.get("/cart", response_class=HTMLResponse)
async def show_cart(
        request: Request,
        cart: Annotated[dict[UUID, int], Depends(cart_to_dict)],
        token: str | None = Cookie(default=None)
):
    global cart_amount
    cart_amount = 0
    products = []

    if cart:
        db_products = await get_products_by_uuids(uuids=cart.keys())

        for product in db_products:
            total_price = cart[product.uuid] * product.price

            products.append(ProductInCart(
                uuid=product.uuid,
                name=product.name,
                price=product.price,
                quantity=product.quantity,
                seller_username=product.seller_username,
                seller_uuid=product.seller_uuid,
                quantity_in_cart=cart[product.uuid],
                total_price=total_price
            ))

            cart_amount += total_price


    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "products": products,
            "cart_amount": cart_amount,
            "token": token
        }
    )


@router.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    login = ""

    if login:
        return templates.TemplateResponse("offer.html", {"request": request, "cart_amount": cart_amount})
    else:
        return RedirectResponse("/login", status_code=303)