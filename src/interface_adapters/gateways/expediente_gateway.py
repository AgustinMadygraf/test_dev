"""
Path: src/interface_adapters/gateways/expediente_gateway.py
"""

from typing import List, Optional, Any, Dict, Protocol
from src.domain.entidades.expediente import Expediente
from src.domain.servicios.repositorios import IRepositorioExpediente

class DatabaseAdapter(Protocol):
    def save(self, data: Dict[str, Any]) -> Dict[str, Any]: ...
    def find_by_numero(self, numero: str) -> Optional[Dict[str, Any]]: ...
    def find_by_id(self, id: int) -> Optional[Dict[str, Any]]: ...
    def find_all(self) -> List[Dict[str, Any]]: ...

class ExpedienteGateway(IRepositorioExpediente):
    def __init__(self, db_adapter: DatabaseAdapter):
        self.db = db_adapter

    def save(self, expediente: Expediente) -> Expediente:
        data: Dict[str, Any] = {
            "numero": expediente.numero,
            "extracto": expediente.extracto,
            "id_propietario": expediente.id_propietario,
            "descripcion": expediente.descripcion
        }
        if expediente.id is not None:
            data["id"] = expediente.id
        persisted_data = self.db.save(data)
        return self._map_to_entity(persisted_data)

    def get_by_numero(self, numero: str) -> Optional[Expediente]:
        data = self.db.find_by_numero(numero)
        return self._map_to_entity(data) if data else None

    def get_by_id(self, expediente_id: int) -> Optional[Expediente]:
        data = self.db.find_by_id(expediente_id)
        return self._map_to_entity(data) if data else None

    def get_all(self) -> List[Expediente]:
        raw_list = self.db.find_all()
        return [self._map_to_entity(item) for item in raw_list]

    def _map_to_entity(self, data: Dict[str, Any]) -> Expediente:
        # Mapeo de Diccionario -> Entidad (Dominio)
        return Expediente(
            id=data.get("id"),
            numero=data["numero"],
            extracto=data["extracto"],
            id_propietario=data["id_propietario"],
            descripcion=data.get("descripcion")
        )