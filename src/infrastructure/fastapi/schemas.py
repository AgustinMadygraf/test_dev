"""
Path: src/infrastructure/fastapi/schemas.py
"""

from pydantic import BaseModel

class ExpedienteResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
