import json

from uuid import UUID

from fastapi import Cookie


def cart_to_dict(cart: str | None = Cookie(default=None)) -> dict[UUID, int]:
    if cart:
        cart: dict = json.loads(cart.replace("'", '"'))
        return {UUID(uuid): cart[uuid] for uuid in cart}
    else:
        return {}