"""
Path: src/use_cases/auth.py
"""

from typing import Optional
from src.domain.entities.user import User
from src.domain.services.unit_of_work import IUnitOfWork
from src.domain.services.security import ISecurityService

class AuthUseCases:
    def __init__(self, uow: IUnitOfWork, security_service: ISecurityService):
        self.uow = uow
        self.security_service = security_service

    def register(self, email: str, password: str, full_name: Optional[str] = None) -> User:
        with self.uow:
            # 1. Verificar si el usuario ya existe
            existing_user = self.uow.users.get_by_email(email)
            if existing_user:
                raise ValueError("El correo electrónico ya está registrado")

            # 2. Hashear la contraseña (Infrastructura vía Abstracción)
            hashed_password = self.security_service.get_password_hash(password)

            # 3. Crear entidad y persistir
            new_user = User(email=email, hashed_password=hashed_password, full_name=full_name)
            created_user = self.uow.users.save(new_user)
            return created_user

    def login(self, email: str, password: str) -> dict:
        with self.uow:
            user = self.uow.users.get_by_email(email)
            
            if not user or not self.security_service.verify_password(password, user.hashed_password):
                raise ValueError("Credenciales inválidas")
            
            if not user.is_active:
                raise ValueError("Usuario inactivo")
            
            access_token = self.security_service.create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        