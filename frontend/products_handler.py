from fastapi import APIRouter, Form
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

import frontend.database


router = APIRouter()

templates = Jinja2Templates(directory="frontend/html")


@router.post("/update_cart")
async def update_cart(endpoint_url: str = Form(...), product_id: str = Form(...), action: str = Form(...)):
    if action == "increase":
        frontend.database.insert_into_cart(id=product_id)
    else:
        frontend.database.insert_into_cart(id=product_id, count=-1)
    return RedirectResponse(endpoint_url, status_code=303)