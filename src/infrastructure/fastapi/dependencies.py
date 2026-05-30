"""
Path: src/infrastructure/fastapi/dependencies.py
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.infrastructure.sqlalchemy.database import SessionLocal
from src.infrastructure.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from src.domain.services.unit_of_work import IUnitOfWork
from src.use_cases.expediente import ExpedienteUseCases
from src.use_cases.auth import AuthUseCases
from src.domain.services.security import ISecurityService
from src.infrastructure.settings.security import decode_access_token, JWTSecurityService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_uow() -> IUnitOfWork:
    return SQLAlchemyUnitOfWork(SessionLocal)

def get_expediente_use_cases(uow: IUnitOfWork = Depends(get_uow)) -> ExpedienteUseCases:
    return ExpedienteUseCases(uow)

def get_security_service() -> ISecurityService:
    return JWTSecurityService()

def get_auth_use_cases(
    uow: IUnitOfWork = Depends(get_uow),
    security_service: ISecurityService = Depends(get_security_service)
) -> AuthUseCases:
    return AuthUseCases(uow, security_service)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: IUnitOfWork = Depends(get_uow)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    with uow:
        user = uow.users.get_by_email(email)
        if user is None:
            raise credentials_exception
        return user
