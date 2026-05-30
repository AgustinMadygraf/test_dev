"""
Path: src/infrastructure/settings/settings.py
"""

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    """Configuración centralizada de la infraestructura."""
    
    # Base de Datos
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "expedientes_db")

    # App Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    @property
    def database_url(self) -> str:
        """Genera el DSN para SQLAlchemy o cualquier driver MySQL."""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Instancia única para ser importada por los adaptadores de infraestructura
settings = Settings()
