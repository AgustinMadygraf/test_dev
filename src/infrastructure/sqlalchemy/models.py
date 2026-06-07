"""
Path: src/infrastructure/sqlalchemy/models.py
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import declarative_base
from src.domain.entidades.expediente import EstadoExpediente
from datetime import datetime, timezone

Base = declarative_base()

class ExpedienteORM(Base):
    __tablename__ = "expedientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(String(50), unique=True, nullable=False)
    extracto = Column(String(255), nullable=False)
    id_propietario = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ultima_modificacion = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    estado = Column(Enum(EstadoExpediente), default=EstadoExpediente.BORRADOR)

class UsuarioORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    correo = Column(String(255), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(255), nullable=True)
    es_activo = Column(Boolean, default=True)
    es_administrador = Column(Boolean, default=False)