# Path: src/aplicacion/expediente.py

from typing import List, Optional
from src.dominio.entidades.expediente import Expediente
from src.aplicacion.servicios.unidad_de_trabajo import UnidadDeTrabajo
from src.dominio.excepciones import ErrorViolacionReglaNegocio

class CasosUsoExpediente:
    def __init__(self, uow: UnidadDeTrabajo):
        self.uow = uow

    def crear_expediente(self, numero: str, extracto: str, id_propietario: int, descripcion: Optional[str] = None) -> Expediente:
        with self.uow:
            existente = self.uow.expedientes.buscar_por_numero(numero)
            if existente:
                raise ErrorViolacionReglaNegocio(f"El expediente con número {numero} ya existe.")
            
            nuevo_expediente = Expediente.crear_nuevo(
                numero=numero,
                extracto=extracto,
                id_propietario=id_propietario,
                descripcion=descripcion
            )
            resultado = self.uow.expedientes.guardar(nuevo_expediente)
            return resultado

    def listar_expedientes(self, id_propietario: Optional[int] = None) -> List[Expediente]:
        with self.uow:
            return self.uow.expedientes.buscar_todos(id_propietario=id_propietario)

    def obtener_expediente(self, expediente_id: int) -> Optional[Expediente]:
        with self.uow:
            return self.uow.expedientes.buscar_por_id(expediente_id)
