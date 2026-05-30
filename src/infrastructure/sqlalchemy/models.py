"""
Path: src/infrastructure/sqlalchemy/models.py
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import declarative_base
from src.domain.entities.expediente import ExpedienteStatus
from datetime import datetime, timezone

Base = declarative_base()

class ExpedienteORM(Base):
    __tablename__ = "expedientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(String(50), unique=True, nullable=False)
    extracto = Column(String(255), nullable=False)
    owner_id = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ultima_modificacion = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    estado = Column(Enum(ExpedienteStatus), default=ExpedienteStatus.BORRADOR)

class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)