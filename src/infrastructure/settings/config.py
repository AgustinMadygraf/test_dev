"""
Path: src/infrastructure/settings/config.py
"""

import os
from typing import List, Any, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Base de Datos
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "expedientes.sqlite"

    # App Settings
    APP_TITLE: str = "Expediente Management System API"
    APP_DESCRIPTION: str = "API for Expediente Management System"
    APP_VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"

    # CORS Settings
    CORS_ORIGINS: Union[List[str], str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: Union[List[str], str] = ["*"]
    CORS_ALLOW_HEADERS: Union[List[str], str] = ["*"]

    @field_validator("CORS_ORIGINS", "CORS_ALLOW_METHODS", "CORS_ALLOW_HEADERS", mode="before")
    @classmethod
    def parse_comma_separated_list(cls, v: Any) -> Any:
        if isinstance(v, str) and not v.startswith(("[", "{")):
            return [i.strip() for i in v.split(",")]
        return v

    @property
    def database_url(self) -> str:
        """Genera el DSN. Si no hay host configurado, asume SQLite para el MVP."""
        if not self.DB_HOST or self.DB_HOST == "localhost":
            # Aseguramos que el archivo se guarde en una carpeta 'data' relativa a la raíz
            data_dir = "./data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            return f"sqlite:///{data_dir}/{self.DB_NAME}"
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Instancia única para ser importada por los adaptadores de infraestructura
settings = Settings()
