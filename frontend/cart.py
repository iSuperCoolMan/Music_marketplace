from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from frontend.requests_to_api import *
from frontend.products_handler import router as products_router

import frontend.database


router = APIRouter()
router.include_router(products_router)

templates = Jinja2Templates(directory="frontend/html")

cart_amount = 0


@router.get("/cart", response_class=HTMLResponse)
async def get_cart(request: Request):
    global cart_amount

    ids = list(frontend.database.get_ids_from_cart())
    products = await get_products_by_id(ids)

    cart_amount = 0

    for product in products:
        product["count"] = frontend.database.get_count_from_cart(id=product["id"])
        product["total_price"] = product["count"] * product["price"]
        cart_amount += product["total_price"]

    print(cart_amount)

    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "products": products,
            "cart_amount": cart_amount,
            "token": frontend.cookies.user["token"]
        }
    )


@router.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    login = ""

    if login:
        return templates.TemplateResponse("offer.html", {"request": request, "cart_amount": cart_amount})
    else:
        return RedirectResponse("/login", status_code=303)