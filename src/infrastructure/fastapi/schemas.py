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

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
