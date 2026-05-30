"""
Path: src/domain/entities/expediente.py
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

class ExpedienteStatus(Enum):
    BORRADOR = "borrador"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    ARCHIVADO = "archivado"

@dataclass
class Expediente:
    numero: str
    extracto: str
    owner_id: int
    id: Optional[int] = None
    descripcion: Optional[str] = None
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ultima_modificacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    estado: ExpedienteStatus = ExpedienteStatus.BORRADOR

    def __repr__(self) -> str:
        return f"<Expediente(numero={self.numero}, estado={self.estado})>"