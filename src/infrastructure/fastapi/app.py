"""
Path: src/infrastructure/fastapi/app.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

async def health_check():
    return {"status": "ok", "message": "Service is running"}

async def read_root():
    return {"message": "Bienvenido al Sistema de Gestión de Expedientes API", "version": "0.1.0"}

def create_app() -> FastAPI:
    app = FastAPI(
        title="Sistema de Gestión de Expedientes",
        description="API para la gestión de expedientes administrativos y legales.",
        version="0.1.0"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.get("/", tags=["System"])(read_root)
    app.get("/health", tags=["System"])(health_check)

    return app

app = create_app()
