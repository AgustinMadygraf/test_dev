"""
Path: src/infrastructure/fastapi/app.py
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, Request, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.sqlalchemy.database import init_db
from src.infrastructure.fastapi.routes import router as expediente_router
from src.infrastructure.fastapi.auth_routes import router as auth_router
from src.infrastructure.settings.config import settings
from src.infrastructure.settings.logger import get_logger

logger = get_logger(__name__, settings.LOG_LEVEL)

STATIC_FILE = os.path.join(os.path.dirname(__file__), "static", "index.html")
STATIC_DIR = os.path.dirname(STATIC_FILE)
LOGIN_FILE = os.path.join(STATIC_DIR, "login.html")
REGISTER_FILE = os.path.join(STATIC_DIR, "register.html")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        logger.info("Base de datos inicializada correctamente.")
        os.makedirs(os.path.dirname(STATIC_FILE), exist_ok=True)
    except Exception as e:
        logger.error(f"ERROR CRÍTICO: No se pudo conectar a la base de datos: {e}")
    yield

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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
async def read_root():
    if os.path.exists(STATIC_FILE):
        return FileResponse(STATIC_FILE)
    return {"message": "API is running. Frontend file not found at src/infrastructure/fastapi/static/index.html"}

@app.get("/login", tags=["System"])
async def read_login():
    if os.path.exists(LOGIN_FILE):
        return FileResponse(LOGIN_FILE)
    return JSONResponse(status_code=404, content={"message": "Login file not found"})

@app.get("/register", tags=["System"])
async def read_register():
    if os.path.exists(REGISTER_FILE):
        return FileResponse(REGISTER_FILE)
    return JSONResponse(status_code=404, content={"message": "Register file not found"})


from src.domain.exceptions import BusinessRuleViolationError

@app.exception_handler(BusinessRuleViolationError)
async def business_rule_violation_exception_handler(request: Request, exc: BusinessRuleViolationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

app.include_router(auth_router)
app.include_router(expediente_router)
