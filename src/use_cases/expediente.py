"""
Path: src/use_cases/expediente.py
"""

from typing import List, Optional
from src.domain.entities.expediente import Expediente
from src.domain.services.repositories import IExpedienteRepository

class ExpedienteUseCases:
    def __init__(self, repository: IExpedienteRepository):
        self.repository = repository

    def crear_expediente(self, numero: str, extracto: str, owner_id: int, descripcion: Optional[str] = None) -> Expediente:
        existing = self.repository.get_by_numero(numero)
        if existing:
            raise ValueError(f"El expediente con número {numero} ya existe.")
        
        nuevo_expediente = Expediente(
            numero=numero,
            extracto=extracto,
            owner_id=owner_id,
            descripcion=descripcion
        )
        return self.repository.save(nuevo_expediente)

    def listar_expedientes(self) -> List[Expediente]:
        return self.repository.get_all()