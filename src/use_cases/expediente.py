"""
Path: src/use_cases/expediente.py
"""

from typing import List, Optional
from src.domain.entities.expediente import Expediente
from src.domain.services.unit_of_work import IUnitOfWork

class ExpedienteUseCases:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def crear_expediente(self, numero: str, extracto: str, owner_id: int, descripcion: Optional[str] = None) -> Expediente:
        with self.uow:
            existing = self.uow.expedientes.get_by_numero(numero)
            if existing:
                raise ValueError(f"El expediente con número {numero} ya existe.")
            
            nuevo_expediente = Expediente(
                numero=numero,
                extracto=extracto,
                owner_id=owner_id,
                descripcion=descripcion
            )
            result = self.uow.expedientes.save(nuevo_expediente)
            return result

    def listar_expedientes(self, owner_id: Optional[int] = None) -> List[Expediente]:
        with self.uow:
            return self.uow.expedientes.get_all(owner_id=owner_id)

    def obtener_expediente(self, expediente_id: int) -> Optional[Expediente]:
        with self.uow:
            return self.uow.expedientes.get_by_id(expediente_id)