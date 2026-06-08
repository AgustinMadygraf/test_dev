# Path: src/infraestructura/settings/security.py

from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import jwt
from passlib.context import CryptContext
from src.aplicacion.servicios.seguridad import IServicioSeguridad
from src.infraestructura.settings.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contrasena(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def obtener_hash_contrasena(password: str) -> str:
    return pwd_context.hash(password)

def crear_token_acceso(datos: dict, delta_expiracion: Optional[timedelta] = None) -> str:
    to_encode = datos.copy()
    if delta_expiracion:
        expire = datetime.now(timezone.utc) + delta_expiracion
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload if payload.get("sub") else None
    except Exception:
        return None

class JWTSecurityService(IServicioSeguridad):
    def verificar_contrasena(self, contrasena_plana: str, contrasena_hash: str) -> bool:
        return verificar_contrasena(contrasena_plana, contrasena_hash)

    def obtener_hash_contrasena(self, contrasena: str) -> str:
        return obtener_hash_contrasena(contrasena)

    def crear_token_acceso(self, datos: dict, delta_expiracion: Optional[timedelta] = None) -> str:
        return crear_token_acceso(datos, delta_expiracion)