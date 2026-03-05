import json

from uuid import UUID

from fastapi import APIRouter, Cookie
from fastapi.responses import HTMLResponse
from sqlalchemy.testing.util import total_size
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from db.product import get_products_by_uuids
from models.products import ProductInCart
from settings import directories


router = APIRouter()

templates = Jinja2Templates(directory=directories.TEMPLATE_DIRECTORY)