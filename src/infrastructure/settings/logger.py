"""
Path: src/infrastructure/settings/logger.py
"""

import logging
import sys
from typing import Dict

class UvicornLikeFormatter(logging.Formatter):
    """Formateador que imita la estética de FastAPI/Uvicorn."""
    
    # Colores ANSI
    LEVEL_COLORS: Dict[int, str] = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[31;1m" # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelno, self.RESET)
        
        # Estilo: "INFO:    " (Nivel + Colon + Padding de 5 espacios)
        levelname_styled = f"{color}{record.levelname}:{self.RESET}".ljust(15)
        
        # Construcción del mensaje: Nivel estilizado + Nombre del logger + Mensaje
        # Ejemplo: INFO:     [src.logic] El proceso ha comenzado
        record.levelname = levelname_styled
        
        # Definimos un formato minimalista
        self._style._fmt = "%(levelname)s [%(name)s] %(message)s"
        
        return super().format(record)

def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Configura y devuelve una instancia de logger estandarizada."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(level.upper())
        handler = logging.StreamHandler(sys.stdout)
        formatter = UvicornLikeFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
