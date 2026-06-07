"""
Path: src/interface_adapters/controllers/expediente_controller.py
"""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from src.use_cases.expediente import ExpedienteUseCases
from src.interface_adapters.presenters.expediente_presenter import ExpedientePresenter

@dataclass(frozen=True)
class ExpedienteCreateDTO:
    numero: str
    extracto: str
    id_propietario: int
    descripcion: Optional[str] = None

class ExpedienteController:
    def __init__(self, use_cases: ExpedienteUseCases, presenter: ExpedientePresenter):
        self.use_cases = use_cases
        self.presenter = presenter

    def crear(self, data: Dict[str, Any]) -> Dict[str, Any]:
        dto = ExpedienteCreateDTO(**data)
        
        expediente = self.use_cases.crear_expediente(
            numero=dto.numero,
            extracto=dto.extracto,
            id_propietario=dto.id_propietario,
            descripcion=dto.descripcion
        )
        
        return self.presenter.format(expediente)

    def listar(self) -> List[Dict[str, Any]]:
        expedientes = self.use_cases.listar_expedientes()
        return self.presenter.format_list(expedientes)

    def obtener(self, expediente_id: int) -> Optional[Dict[str, Any]]:
        expediente = self.use_cases.obtener_expediente(expediente_id)
        if not expediente:
            return None
        return self.presenter.format(expediente)
