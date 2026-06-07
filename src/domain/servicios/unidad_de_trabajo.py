from abc import ABC, abstractmethod
from src.domain.servicios.repositorios import IRepositorioExpediente, IRepositorioUsuario

class IUnidadDeTrabajo(ABC):
    expedientes: IRepositorioExpediente
    usuarios: IRepositorioUsuario

    def __enter__(self) -> "IUnidadDeTrabajo":
        return self

    def __exit__(self, tipo_excepcion, valor_excepcion, traceback):
        if tipo_excepcion:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
