# Path: src/aplicacion/servicios/seguridad.py

from abc import ABC, abstractmethod
from typing import Optional
from datetime import timedelta

class IServicioSeguridad(ABC):
    @abstractmethod
    def verificar_contrasena(self, contrasena_plana: str, contrasena_hash: str) -> bool:
        pass

    @abstractmethod
    def obtener_hash_contrasena(self, contrasena: str) -> str:
        pass

    @abstractmethod
    def crear_token_acceso(self, datos: dict, delta_expiracion: Optional[timedelta] = None) -> str:
        pass
