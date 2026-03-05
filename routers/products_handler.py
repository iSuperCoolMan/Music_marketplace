from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Form, Cookie, Depends
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from routers.depends import cart_to_dict
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)


@router.post("/update_cart")
async def update_cart(
        endpoint_url: str,
        product_uuid: UUID,
        action: str,
        cart: Annotated[dict[UUID, int], Depends(cart_to_dict)]
):
    response = RedirectResponse(endpoint_url, status_code=303)

    if action == "increase":
        cart[product_uuid] = cart[product_uuid] + 1
    else:
        cart[product_uuid] = cart[product_uuid] - 1

    response.set_cookie(key="cart", value=str(cart), max_age=3600)
    return response