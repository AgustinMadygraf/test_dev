# Path: src/domain/entities/expediente.py

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Union
from src.domain.value_objects import NumeroExpediente
from src.domain.exceptions import InvalidStateTransitionError

class ExpedienteStatus(Enum):
    BORRADOR = "borrador"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    ARCHIVADO = "archivado"

@dataclass
class Expediente:
    numero: NumeroExpediente
    extracto: str
    owner_id: int
    id: Optional[int] = None
    descripcion: Optional[str] = None
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ultima_modificacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    estado: ExpedienteStatus = ExpedienteStatus.BORRADOR

    def __post_init__(self):
        if isinstance(self.numero, str):
            self.numero = NumeroExpediente(self.numero)

    @classmethod
    def crear_nuevo(cls, numero: Union[str, NumeroExpediente], extracto: str, owner_id: int, descripcion: Optional[str] = None):
        if not isinstance(numero, NumeroExpediente):
            numero = NumeroExpediente(numero)
        return cls(
            numero=numero,
            extracto=extracto,
            owner_id=owner_id,
            descripcion=descripcion,
            estado=ExpedienteStatus.BORRADOR
        )

    def cambiar_estado(self, nuevo_estado: ExpedienteStatus):
        if self.estado == ExpedienteStatus.ARCHIVADO:
            raise InvalidStateTransitionError("No se puede cambiar el estado de un expediente ARCHIVADO")
        
        if self.estado == ExpedienteStatus.FINALIZADO and nuevo_estado == ExpedienteStatus.BORRADOR:
            raise InvalidStateTransitionError("No se puede volver a BORRADOR desde FINALIZADO")

        self.estado = nuevo_estado
        self.ultima_modificacion = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<Expediente(numero={self.numero}, estado={self.estado})>"
