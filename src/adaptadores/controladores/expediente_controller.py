# Path: src/adaptadores/controladores/expediente_controller.py

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from src.aplicacion.expediente import CasosUsoExpediente
from src.adaptadores.presentadores.expediente_presenter import PresentadorExpediente

@dataclass(frozen=True)
class ExpedienteCrearDTO:
    numero: str
    extracto: str
    id_propietario: int
    descripcion: Optional[str] = None

class ControladorExpediente:
    def __init__(self, casos_uso: CasosUsoExpediente, presentador: PresentadorExpediente):
        self.casos_uso = casos_uso
        self.presentador = presentador

    def crear(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        dto = ExpedienteCrearDTO(**datos)
        
        expediente = self.casos_uso.crear_expediente(
            numero=dto.numero,
            extracto=dto.extracto,
            id_propietario=dto.id_propietario,
            descripcion=dto.descripcion
        )
        
        return self.presentador.formatear(expediente)

    def listar(self) -> List[Dict[str, Any]]:
        expedientes = self.casos_uso.listar_expedientes()
        return self.presentador.formatear_lista(expedientes)

    def obtener(self, id_expediente: int) -> Optional[Dict[str, Any]]:
        expediente = self.casos_uso.obtener_expediente(id_expediente)
        if not expediente:
            return None
        return self.presentador.formatear(expediente)
