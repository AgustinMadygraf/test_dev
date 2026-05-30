"""
Path: src/infrastructure/sqlalchemy/database.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.settings.config import settings
from src.infrastructure.sqlalchemy.models import Base

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
