"""
Path: src/infrastructure/fastapi/schemas.py
"""

from pydantic import BaseModel

class ExpedienteResponse(BaseModel):
    numero_referencia: str
    resumen: str
    responsable_id: int
    descripcion_detallada: str
    estado_actual: str
    fecha_apertura: str
    es_editable: bool
