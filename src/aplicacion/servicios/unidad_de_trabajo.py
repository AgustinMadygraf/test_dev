# Path: src/aplicacion/servicios/unidad_de_trabajo.py

from abc import ABC, abstractmethod
from src.dominio.servicios.repositorios import IRepositorioExpediente, IRepositorioUsuario

class UnidadDeTrabajo(ABC):
    expedientes: IRepositorioExpediente
    usuarios: IRepositorioUsuario

    def __enter__(self) -> "UnidadDeTrabajo":
        return self

    def __exit__(self, tipo_excepcion, valor_excepcion, traza):
        if tipo_excepcion:
            self.revertir()
        else:
            self.confirmar()

    @abstractmethod
    def confirmar(self):
        pass

    @abstractmethod
    def revertir(self):
        pass
