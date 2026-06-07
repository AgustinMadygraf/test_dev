# Path: src/dominio/entidades/expediente.py

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Union
from src.dominio.objetos_valor import NumeroExpediente
from src.dominio.excepciones import ErrorTransicionEstadoInvalida

class EstadoExpediente(Enum):
    BORRADOR = "borrador"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    ARCHIVADO = "archivado"

@dataclass
class Expediente:
    numero: NumeroExpediente
    extracto: str
    id_propietario: int
    id: Optional[int] = None
    descripcion: Optional[str] = None
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ultima_modificacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    estado: EstadoExpediente = EstadoExpediente.BORRADOR

    def __post_init__(self):
        if isinstance(self.numero, str):
            self.numero = NumeroExpediente(self.numero)

    @classmethod
    def crear_nuevo(cls, numero: Union[str, NumeroExpediente], extracto: str, id_propietario: int, descripcion: Optional[str] = None):
        if not isinstance(numero, NumeroExpediente):
            numero = NumeroExpediente(numero)
        return cls(
            numero=numero,
            extracto=extracto,
            id_propietario=id_propietario,
            descripcion=descripcion,
            estado=EstadoExpediente.BORRADOR
        )

    def cambiar_estado(self, nuevo_estado: EstadoExpediente):
        if self.estado == EstadoExpediente.ARCHIVADO:
            raise ErrorTransicionEstadoInvalida("No se puede cambiar el estado de un expediente ARCHIVADO")
        
        if self.estado == EstadoExpediente.FINALIZADO and nuevo_estado == EstadoExpediente.BORRADOR:
            raise ErrorTransicionEstadoInvalida("No se puede volver a BORRADOR desde FINALIZADO")

        self.estado = nuevo_estado
        self.ultima_modificacion = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<Expediente(numero={self.numero}, estado={self.estado})>"
