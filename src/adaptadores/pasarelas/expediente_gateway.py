"""
Path: src/adaptadores/pasarelas/expediente_gateway.py
"""

from typing import List, Optional, Any, Dict, Protocol
from datetime import datetime
from src.dominio.entidades.expediente import Expediente, EstadoExpediente
from src.dominio.servicios.repositorios import IRepositorioExpediente

class AdaptadorBaseDeDatos(Protocol):
    def save(self, data: Dict[str, Any]) -> Dict[str, Any]: ...
    def find_by_numero(self, numero: str) -> Optional[Dict[str, Any]]: ...
    def find_by_id(self, id: int) -> Optional[Dict[str, Any]]: ...
    def find_all(self) -> List[Dict[str, Any]]: ...

class PasarelaExpediente(IRepositorioExpediente):
    def __init__(self, adaptador_db: AdaptadorBaseDeDatos):
        self.db = adaptador_db

    def guardar(self, expediente: Expediente) -> Expediente:
        datos: Dict[str, Any] = {
            "numero": expediente.numero,
            "extracto": expediente.extracto,
            "id_propietario": expediente.id_propietario,
            "descripcion": expediente.descripcion,
            "estado": expediente.estado,
            "fecha_creacion": expediente.fecha_creacion,
            "ultima_modificacion": expediente.ultima_modificacion
        }
        if expediente.id is not None:
            datos["id"] = expediente.id
        datos_persistidos = self.db.save(datos)
        return self._mapear_a_entidad(datos_persistidos)

    def buscar_por_numero(self, numero: str) -> Optional[Expediente]:
        datos = self.db.find_by_numero(numero)
        return self._mapear_a_entidad(datos) if datos else None

    def buscar_por_id(self, id_expediente: int) -> Optional[Expediente]:
        datos = self.db.find_by_id(id_expediente)
        return self._mapear_a_entidad(datos) if datos else None

    def buscar_todos(self, id_propietario: Optional[int] = None) -> List[Expediente]:
        lista_bruta = self.db.find_all()
        if id_propietario is not None:
            lista_bruta = [item for item in lista_bruta if item.get("id_propietario") == id_propietario]
        return [self._mapear_a_entidad(item) for item in lista_bruta]

    def _mapear_a_entidad(self, datos: Dict[str, Any]) -> Expediente:
        # Mapeo de Diccionario -> Entidad (Dominio)
        estado_raw = datos.get("estado")
        estado = EstadoExpediente(estado_raw) if isinstance(estado_raw, str) else EstadoExpediente.BORRADOR
        
        fecha_creacion = datos.get("fecha_creacion")
        if not isinstance(fecha_creacion, datetime):
            fecha_creacion = datetime.now()
            
        ultima_modificacion = datos.get("ultima_modificacion")
        if not isinstance(ultima_modificacion, datetime):
            ultima_modificacion = datetime.now()

        return Expediente(
            id=datos.get("id"),
            numero=datos["numero"],
            extracto=datos["extracto"],
            id_propietario=datos["id_propietario"],
            descripcion=datos.get("descripcion"),
            estado=estado,
            fecha_creacion=fecha_creacion,
            ultima_modificacion=ultima_modificacion
        )
