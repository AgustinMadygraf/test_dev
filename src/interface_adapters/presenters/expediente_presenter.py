"""
Path: src/interface_adapters/presenters/expediente_presenter.py
"""

from typing import Any, Dict, List
from src.dominio.entidades.expediente import Expediente

class ExpedientePresenter:
    def format(self, expediente: Expediente) -> Dict[str, Any]:
        return {
            "numero_referencia": expediente.numero,
            "resumen": expediente.extracto.upper(),
            "responsable_id": expediente.id_propietario,
            "descripcion_detallada": expediente.descripcion or "Sin descripción",
            "estado_actual": expediente.estado.value.replace("_", " ").capitalize(),
            "fecha_apertura": expediente.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            "es_editable": expediente.estado.value == "borrador"
        }

    def format_list(self, expedientes: List[Expediente]) -> List[Dict[str, Any]]:
        return [self.format(e) for e in expedientes]
