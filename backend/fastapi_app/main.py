import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi_app.api.v1.router import api_v1_router
from fastapi_app.core.config import settings
from fastapi_app.middleware.exception import exception_middleware
from fastapi_app.middleware.logging import logging_middleware

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s %(name)s — %(message)s",
)


Path("static/avatars").mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan,
)

app.middleware("http")(exception_middleware)
app.middleware("http")(logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static", html=False), name="static")
app.include_router(api_v1_router)
