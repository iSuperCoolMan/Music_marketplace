from fastapi import FastAPI
from frontend.main import router as main_router
from frontend.cart import router as cart_router
from frontend.login import router as login_router
from frontend.register import router as register_router
from frontend.user import router as user_router

app = FastAPI()

app.include_router(main_router)
app.include_router(cart_router)
app.include_router(login_router)
app.include_router(register_router)
app.include_router(user_router)