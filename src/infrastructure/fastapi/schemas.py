from src.domain.value_objects import NumeroExpediente, Email
"""
Path: src/infrastructure/fastapi/schemas.py
"""

from pydantic import BaseModel, ConfigDict, PlainSerializer, BeforeValidator
from typing import Annotated, Optional, Any
from datetime import datetime
from src.domain.entities.expediente import ExpedienteStatus

def validate_numero(value: Any) -> NumeroExpediente:
    if isinstance(value, NumeroExpediente):
        return value
    return NumeroExpediente(valor=str(value))

def validate_email(value: Any) -> Email:
    if isinstance(value, Email):
        return value
    return Email(address=str(value))

NumeroAnnotated = Annotated[NumeroExpediente, BeforeValidator(validate_numero), PlainSerializer(lambda x: str(x), return_type=str)]
EmailAnnotated = Annotated[Email, BeforeValidator(validate_email), PlainSerializer(lambda x: str(x), return_type=str)]

class ExpedienteCreate(BaseModel):
    numero: NumeroAnnotated
    extracto: str
    descripcion: Optional[str] = None

class ExpedienteRead(BaseModel):
    id: int
    numero: NumeroAnnotated
    extracto: str
    owner_id: int
    descripcion: Optional[str] = None
    estado: ExpedienteStatus
    fecha_creacion: datetime
    ultima_modificacion: datetime

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailAnnotated
    password: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailAnnotated
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
