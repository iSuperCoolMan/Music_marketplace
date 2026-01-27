from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from frontend.requests_to_api import *
from frontend.products_handler import router as products_router

import frontend.database
import frontend.cookies


router = APIRouter()
router.include_router(products_router)

templates = Jinja2Templates(directory="frontend/html")


@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    products = await get_all_products()
    cart_ids = frontend.database.get_ids_from_cart()

    for product in products:
        if product["id"] in cart_ids:
            product["in_cart"] = frontend.database.get_count_from_cart(product["id"])
        else:
            product["in_cart"] = 0

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "products": products,
            "token": frontend.cookies.user["token"]
        }
    )


@router.post("/add_to_cart")
async def add_to_cart(product_id: str = Form(...)):
    frontend.database.insert_into_cart(id=product_id)
    return RedirectResponse('/', status_code=303)

