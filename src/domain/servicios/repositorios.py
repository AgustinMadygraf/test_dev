from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entidades.usuario import Usuario
from src.domain.entidades.expediente import Expediente

class IRepositorioUsuario(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def buscar_por_correo(self, correo: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:
        pass

class IRepositorioExpediente(ABC):
    @abstractmethod
    def guardar(self, expediente: Expediente) -> Expediente:
        pass

    @abstractmethod
    def buscar_todos(self, id_propietario: Optional[int] = None) -> List[Expediente]:
        pass

    @abstractmethod
    def buscar_por_numero(self, numero: str) -> Optional[Expediente]:
        pass

    @abstractmethod
    def buscar_por_id(self, id_expediente: int) -> Optional[Expediente]:
        pass
