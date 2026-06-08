"""
Path: src/infraestructura/sqlalchemy/database.py
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from src.infraestructura.settings.config import settings
from src.infraestructura.sqlalchemy.models import Base
from src.infraestructura.settings.logger import get_logger

logger = get_logger(__name__, settings.LOG_LEVEL)

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise
