# Path: src/adaptadores/presentadores/expediente_presenter.py

from typing import Any, Dict, List
from src.dominio.entidades.expediente import Expediente

class PresentadorExpediente:
    def formatear(self, expediente: Expediente) -> Dict[str, Any]:
        return {
            "numero_referencia": str(expediente.numero),
            "resumen": expediente.extracto.upper(),
            "id_propietario": expediente.id_propietario,
            "descripcion_detallada": expediente.descripcion or "Sin descripción",
            "estado_actual": expediente.estado.value.replace("_", " ").capitalize(),
            "fecha_apertura": expediente.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            "es_editable": expediente.estado.value == "borrador"
        }

    def formatear_lista(self, expedientes: List[Expediente]) -> List[Dict[str, Any]]:
        return [self.formatear(e) for e in expedientes]
