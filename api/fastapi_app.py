from fastapi import FastAPI
from api.products import router as products_router
from api.login import router as login_router


app = FastAPI()

app.include_router(products_router)
app.include_router(login_router)