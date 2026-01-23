from typing import List, Optional
from fastapi import Request, APIRouter
from fastapi.params import Query

import api.database
from api.token_handler import get_current_user

router = APIRouter()


@router.get("/api/products")
async def get_all_products():
    return api.database.get_all_products()


@router.get("/api/products/by_ids")
async def get_products_by_ids(ids: Optional[List[str]] = Query(None)):
    products = []

    if ids:
        for id in ids:
            print(f"{id} send to database")
            products.append(api.database.get_product(id))

    return products


@router.get("/api/products/by_token")
async def get_products_by_user_token(token: Optional[str] = Query(None)):
    user = await get_current_user(token)
    products = []

    if user:
        products = api.database.get_products_by_username(user["username"])
        print(f"{user["username"]} products gotten from database")

    return products


@router.post("/api/products/post")
async def post_product_in_shop(request: Request):
    form = await request.form()
    name = form.get("name")
    seller_token = form.get("seller_token")
    price = form.get("price")
    count = form.get("count")

    print("Received data:", form)

    user = await get_current_user(seller_token)

    api.database.post_product(name, user["username"], price, count)

    return True


@router.post("/api/products/order")
async def post_order(request: Request):
    data = await request.json()
    print("Received data:", data)

    return data



