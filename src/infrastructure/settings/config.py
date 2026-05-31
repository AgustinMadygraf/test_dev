"""
Path: src/infrastructure/settings/config.py
"""

import os
from typing import List, Any, Union, Optional
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
    DB_NAME: str = "sql_app.db"
    DATABASE_URL: str = ""

    # Credenciales Admin (Seeding)
    ADMIN_EMAIL: str = ""
    ADMIN_PASSWORD: str = ""

    # Security Settings
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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

    @field_validator("ADMIN_EMAIL", "ADMIN_PASSWORD", "SECRET_KEY")
    @classmethod
    def check_required_settings(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Este campo es obligatorio. Verificá tu archivo .env")
        return v

    @property
    def database_url(self) -> str:
        # Si se proporciona una URL completa, la usamos
        if self.DATABASE_URL:
            # Si es SQLite, nos aseguramos de que el directorio exista
            if self.DATABASE_URL.startswith("sqlite"):
                # Intentamos extraer el directorio del path de sqlite
                # sqlite:///./data/sql_app.db -> ./data/sql_app.db
                db_path = self.DATABASE_URL.replace("sqlite:///", "")
                db_dir = os.path.dirname(db_path)
                if db_dir and not os.path.exists(db_dir):
                    os.makedirs(db_dir)
            return self.DATABASE_URL
        
        # Si no hay DATABASE_URL, construimos una basada en el host
        if not self.DB_HOST or self.DB_HOST == "localhost":
            data_dir = "./data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            return f"sqlite:///{data_dir}/{self.DB_NAME}"
            
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
