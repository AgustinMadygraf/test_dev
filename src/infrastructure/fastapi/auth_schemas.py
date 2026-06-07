"""
Path: src/infrastructure/fastapi/auth_schemas.py
"""

from pydantic import BaseModel
from typing import Optional
from src.infrastructure.fastapi.schemas import CorreoElectronicoAnnotated

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    username: CorreoElectronicoAnnotated
    password: str
