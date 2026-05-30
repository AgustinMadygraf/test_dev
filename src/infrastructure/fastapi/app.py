"""
Path: src/infrastructure/fastapi/app.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.sqlalchemy.database import init_db
from src.infrastructure.fastapi.expediente import router as expediente_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Expediente Management System API",
    description="API for Expediente Management System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    """Maneja excepciones de valor (reglas de negocio) de forma global."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

app.include_router(expediente_router)
