"""
Path: src/infrastructure/fastapi/app.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.sqlalchemy.database import init_db
from src.infrastructure.fastapi.routes import router as expediente_router
from src.infrastructure.settings.config import settings
from src.infrastructure.settings.logger import get_logger

logger = get_logger(__name__, settings.LOG_LEVEL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        logger.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"ERROR CRÍTICO: No se pudo conectar a la base de datos: {e}")
    yield

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)   

@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(status_code=204)

@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "Service is running"}

@app.get("/", tags=["System"])
async def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Expediente Management System API!"}


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

app.include_router(expediente_router)
