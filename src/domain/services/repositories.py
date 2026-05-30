"""
Path: src/domain/services/repositories.py
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.user import User
from src.domain.entities.expediente import Expediente

class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        """Persiste un usuario en el sistema (Crear o Actualizar)."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su correo electrónico."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID único."""
        pass

class IExpedienteRepository(ABC):
    @abstractmethod
    def save(self, expediente: Expediente) -> Expediente:
        """Persiste un expediente en el sistema."""
        pass

    @abstractmethod
    def get_all(self, owner_id: Optional[int] = None) -> List[Expediente]:
        """Recupera todos los expedientes registrados, opcionalmente filtrados por dueño."""
        pass

    @abstractmethod
    def get_by_numero(self, numero: str) -> Optional[Expediente]:
        """Busca un expediente por su número identificador."""
        pass

    @abstractmethod
    def get_by_id(self, expediente_id: int) -> Optional[Expediente]:
        """Busca un expediente por su ID interno."""
        pass