"""
Path: src/infrastructure/fastapi/app.py
"""

from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.fastapi.schemas import ExpedienteResponse

from src.infrastructure.database import InMemoryDatabaseAdapter
from src.interface_adapters.gateways.expediente_gateway import ExpedienteGateway
from src.use_cases.expediente import ExpedienteUseCases
from src.interface_adapters.controllers.expediente_controller import ExpedienteController
from src.interface_adapters.presenters.expediente_presenter import ExpedientePresenter

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

# Inyección de dependencias y cableado de Clean Architecture
db_adapter = InMemoryDatabaseAdapter()
expediente_repository = ExpedienteGateway(db_adapter=db_adapter)
use_cases = ExpedienteUseCases(repository=expediente_repository)
presenter = ExpedientePresenter()
controller = ExpedienteController(use_cases=use_cases, presenter=presenter)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(status_code=204)

@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "Service is running"}

@app.get("/", tags=["System"])
async def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Expediente Management System API!"}

# El Controller/Presenter manejan la petición y respuesta siguiendo Clean Architecture
@app.get("/expedientes/{expediente_id}", response_model=ExpedienteResponse, tags=["Expedientes"])
async def get_expediente(expediente_id: int) -> dict:
    # El controlador maneja la orquestación y retorna el expediente ya presentado
    expediente_presentado = controller.obtener(expediente_id)
    if not expediente_presentado:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")

    return expediente_presentado
