"""
Path: src/domain/services/unit_of_work.py
"""

from abc import ABC, abstractmethod
from src.domain.services.repositories import IExpedienteRepository

class IUnitOfWork(ABC):
    expedientes: IExpedienteRepository

    def __enter__(self) -> "IUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass