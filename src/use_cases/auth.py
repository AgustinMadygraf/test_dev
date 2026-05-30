"""
Path: src/use_cases/auth.py
"""

from src.domain.services.unit_of_work import IUnitOfWork
from src.domain.services.security import ISecurityService

class AuthUseCases:
    def __init__(self, uow: IUnitOfWork, security_service: ISecurityService):
        self.uow = uow
        self.security_service = security_service

    def login(self, email: str, password: str) -> dict:
        with self.uow:
            user = self.uow.users.get_by_email(email)
            
            if not user or not self.security_service.verify_password(password, user.hashed_password):
                raise ValueError("Credenciales inválidas")
            
            if not user.is_active:
                raise ValueError("Usuario inactivo")
            
            access_token = self.security_service.create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        