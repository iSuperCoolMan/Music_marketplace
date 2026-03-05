from pydantic import BaseModel


class Directories(BaseModel):
    DB_DIRECTORY: str
    TEMPLATE_DIRECTORY: str


class TokenSettings(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int


class MiddlewareSettings(BaseModel):
    ORIGINS: list[str]
    CREDENTIALS: bool
    METHODS: list[str]
    HEADERS: list[str]


directories = Directories(
    DB_DIRECTORY="sqlite:///db/database.db",
    TEMPLATE_DIRECTORY="html"
)

token_settings = TokenSettings(
    SECRET_KEY=open(".venv/login_token.txt", "r").read(),
    ALGORITHM="HS256",
    EXPIRE_MINUTES=30
)

middleware_settings = MiddlewareSettings(
    ORIGINS=[
        'http://localhost:8000', 'http://127.0.0.1:8000',
        'https://localhost:8000', 'https://127.0.0.1:8000'
    ],
    CREDENTIALS=True,
    METHODS=["*"],
    HEADERS=["*"],
)

