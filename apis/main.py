from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.services.authfunctions import database
from .routers.signup import view as view1
from .routers.login import view as view2
from .routers.signout import view as view3
from .routers.getexercises import view as view4
from .routers.getexercises_setting import view as view5
from .routers.addexercises import view as view6
from .routers.addexercises_setting import view as view7
from .routers.getuser import view as view8
import os

is_with_proxy = os.getenv("VITE_REACT_APP_IS_WITH_PROXY")
if is_with_proxy == "True":
    # コンテナ単体の.envでは宣言せず、ルートの.envだけで宣言すると正しく読み込まれる。
    app = FastAPI(
        root_path="/fastapi",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
else:
    app = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")

# app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# AWSなどにデプロイしURLのドメインが確定したら指定する。
# ブラウザからのリクエストはdockerコンテナのサービス名に基づくURLを名前解決できない。
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://frontend.local.dev:4443"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 起動時・終了時にデータベースと接続
@asynccontextmanager
async def app_lifespan(app):
    await startup_logic()
    yield
    await shutdown_logic()


async def startup_logic():
    print("Connecting to the database")
    await database.connect()


async def shutdown_logic():
    print("Disconnecting from the database")
    await database.disconnect()


app.router.lifespan_context = app_lifespan

for v in [view1, view2, view3, view4, view5, view6, view7, view8]:
    app.include_router(v.router)
