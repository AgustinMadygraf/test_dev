"""
Path: src/interface_adapters/controllers/expediente_controller.py
"""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from src.use_cases.expediente import ExpedienteUseCases

@dataclass(frozen=True)
class ExpedienteCreateDTO:
    numero: str
    extracto: str
    owner_id: int
    descripcion: Optional[str] = None

class ExpedienteController:
    def __init__(self, use_cases: ExpedienteUseCases):
        self.use_cases = use_cases

    def crear(self, data: Dict[str, Any]) -> Dict[str, Any]:
        dto = ExpedienteCreateDTO(**data)
        
        expediente = self.use_cases.crear_expediente(
            numero=dto.numero,
            extracto=dto.extracto,
            owner_id=dto.owner_id,
            descripcion=dto.descripcion
        )
        
        return asdict(expediente)

    def listar(self) -> List[Dict[str, Any]]:
        expedientes = self.use_cases.listar_expedientes()
        return [asdict(e) for e in expedientes]
