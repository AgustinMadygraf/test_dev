"""
Path: src/infrastructure/fastapi/app.py
"""

from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.fastapi.schemas import ExpedienteResponse

app = FastAPI(
    title="Expediente Management System API",
    description="API for Expediente Management System",
    version="1.0.0",
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

# El Controller (Maneja la petición y usa el Presenter como response_model)
@app.get("/expedientes/{expediente_id}", response_model=ExpedienteResponse, tags=["Expedientes"])
async def get_expediente(expediente_id: int) -> ExpedienteResponse:
    # Por ahora simulamos la data. En el siguiente paso, esto vendrá de un Gateway.
    if expediente_id <= 0:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")

    return ExpedienteResponse(
        id=expediente_id,
        titulo=f"Expediente #{expediente_id}",
        descripcion="Información recuperada del sistema",
        estado="activo"
    )
