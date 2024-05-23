from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ddd.router.signup import view as view1
from ddd.router.login import view as view2
from ddd.router.logout import view as view3
from ddd.router.getuser import view as view4
from ddd.router.addexercises_setting import view as view5
from ddd.router.getexercises_setting import view as view6
from ddd.router.addexercises import view as view7
from ddd.router.getexercises import view as view8
from ddd.router.getcalendars import view as view9

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


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://frontend.local.dev:4443"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for v in [view1, view2, view3, view4, view5, view6, view7, view8, view9]:
    app.include_router(v.router)
