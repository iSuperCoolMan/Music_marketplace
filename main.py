from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from routers.main import router as main_router
from routers.register import router as register_router
from routers.login import router as login_router
from routers.user import router as user_router
from routers.cart import router as cart_router
from routers.support_chat import router as support_chat_router
from routers.support_page import router as support_page_router
from settings import middleware_settings


app = FastAPI()


@app.middleware("http")
async def print_cookies(request: Request, call_next):
    # print(f"  log  headers = {request.headers}")
    print(f"  log  cookies = {request.cookies}")

    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=middleware_settings.ORIGINS,
    allow_credentials=middleware_settings.CREDENTIALS,
    allow_methods=middleware_settings.METHODS,
    allow_headers=middleware_settings.HEADERS,
)

app.include_router(main_router)
app.include_router(support_chat_router)
app.include_router(cart_router)
app.include_router(register_router)
app.include_router(login_router)
app.include_router(user_router)
app.include_router(support_page_router)