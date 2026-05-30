"""
Path: src/infrastructure/fastapi/schemas.py
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from src.domain.entities.expediente import ExpedienteStatus

class ExpedienteCreate(BaseModel):
    numero: str
    extracto: str
    owner_id: int
    descripcion: Optional[str] = None

class ExpedienteRead(BaseModel):
    id: int
    numero: str
    extracto: str
    owner_id: int
    descripcion: Optional[str] = None
    estado: ExpedienteStatus
    fecha_creacion: datetime
    ultima_modificacion: datetime

    model_config = ConfigDict(from_attributes=True)
