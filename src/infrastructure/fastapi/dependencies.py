"""
Path: src/infrastructure/fastapi/dependencies.py
"""

from fastapi import Depends
from src.infrastructure.sqlalchemy.database import SessionLocal
from src.infrastructure.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from src.domain.services.unit_of_work import IUnitOfWork
from src.use_cases.expediente import ExpedienteUseCases

def get_uow() -> IUnitOfWork:
    """
    Provee una instancia de Unit of Work.
    El ciclo de vida de la sesión se gestiona dentro del contexto del UoW.
    """
    return SQLAlchemyUnitOfWork(SessionLocal)

def get_expediente_use_cases(uow: IUnitOfWork = Depends(get_uow)) -> ExpedienteUseCases:
    """
    Provee la capa de aplicación (Casos de Uso) con su dependencia inyectada.
    """
    return ExpedienteUseCases(uow)