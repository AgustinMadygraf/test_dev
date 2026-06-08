from src.dominio.objetos_valor import NumeroExpediente, CorreoElectronico
"""
Path: src/infraestructura/fastapi/schemas.py
"""

from pydantic import BaseModel, ConfigDict, PlainSerializer, BeforeValidator
from typing import Annotated, Optional, Any
from datetime import datetime
from src.dominio.entidades.expediente import EstadoExpediente

def validate_numero(value: Any) -> NumeroExpediente:
    if isinstance(value, NumeroExpediente):
        return value
    return NumeroExpediente(valor=str(value))

def validate_correo(value: Any) -> CorreoElectronico:
    if isinstance(value, CorreoElectronico):
        return value
    return CorreoElectronico(direccion=str(value))

NumeroAnnotated = Annotated[NumeroExpediente, BeforeValidator(validate_numero), PlainSerializer(lambda x: str(x), return_type=str)]
CorreoElectronicoAnnotated = Annotated[CorreoElectronico, BeforeValidator(validate_correo), PlainSerializer(lambda x: str(x), return_type=str)]

class ExpedienteCreate(BaseModel):
    numero: NumeroAnnotated
    extracto: str
    descripcion: Optional[str] = None

class ExpedienteRead(BaseModel):
    id: int
    numero: NumeroAnnotated
    extracto: str
    id_propietario: int
    descripcion: Optional[str] = None
    estado: EstadoExpediente
    fecha_creacion: datetime
    ultima_modificacion: datetime

    model_config = ConfigDict(from_attributes=True)

class UsuarioCreate(BaseModel):
    correo: CorreoElectronicoAnnotated
    contrasena: str
    nombre_completo: Optional[str] = None

class UsuarioRead(BaseModel):
    id: int
    correo: CorreoElectronicoAnnotated
    nombre_completo: Optional[str] = None
    es_activo: bool
    es_administrador: bool

    model_config = ConfigDict(from_attributes=True)
