"""
Path: src/infrastructure/sqlalchemy/adapter.py
"""

from typing import List, Optional, Any, cast
from src.domain.entities.expediente import Expediente
from src.domain.entities.user import User
from src.domain.services.repositories import IExpedienteRepository, IUserRepository
from src.infrastructure.sqlalchemy.models import ExpedienteORM, UserORM
from sqlalchemy.orm import Session

class SQLAlchemyDatabaseAdapter(IExpedienteRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, expediente: Expediente) -> Expediente:
        if expediente.id:
            obj = self.session.get(ExpedienteORM, expediente.id)
            if obj:
                orm_obj = cast(Any, obj)
                orm_obj.numero = expediente.numero
                orm_obj.extracto = expediente.extracto
                orm_obj.descripcion = expediente.descripcion
                orm_obj.estado = expediente.estado
                orm_obj.owner_id = expediente.owner_id
                self.session.flush()
                return self._to_entity(obj)
        
        new_obj = ExpedienteORM(
            numero=expediente.numero,
            extracto=expediente.extracto,
            owner_id=expediente.owner_id,
            descripcion=expediente.descripcion,
            estado=expediente.estado
        )
        self.session.add(new_obj)
        self.session.flush()
        self.session.refresh(new_obj)
        return self._to_entity(new_obj)

    def get_by_numero(self, numero: str) -> Optional[Expediente]:
        obj = self.session.query(ExpedienteORM).filter_by(numero=numero).first()
        return self._to_entity(obj) if obj else None

    def get_by_id(self, expediente_id: int) -> Optional[Expediente]:
        obj = self.session.get(ExpedienteORM, expediente_id)
        return self._to_entity(obj) if obj else None

    def get_all(self) -> List[Expediente]:
        objs = self.session.query(ExpedienteORM).all()
        return [self._to_entity(obj) for obj in objs]

    def _to_entity(self, orm: ExpedienteORM) -> Expediente:
        """Convierte un objeto ORM de SQLAlchemy a una Entidad de Dominio."""
        return Expediente(
            id=cast(Any, orm.id),
            numero=cast(Any, orm.numero),
            extracto=cast(Any, orm.extracto),
            owner_id=cast(Any, orm.owner_id),
            descripcion=cast(Any, orm.descripcion),
            estado=cast(Any, orm.estado),
            fecha_creacion=cast(Any, orm.fecha_creacion),
            ultima_modificacion=cast(Any, orm.ultima_modificacion)
        )

class SQLAlchemyUserAdapter(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        if user.id:
            obj = self.session.get(UserORM, user.id)
            if obj:
                orm_obj = cast(Any, obj)
                orm_obj.email = user.email
                orm_obj.hashed_password = user.hashed_password
                orm_obj.full_name = user.full_name
                orm_obj.is_active = user.is_active
                orm_obj.is_admin = user.is_admin
                self.session.flush()
                return self._to_entity(obj)
        
        new_obj = UserORM(
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_admin=user.is_admin
        )
        self.session.add(new_obj)
        self.session.flush()
        self.session.refresh(new_obj)
        return self._to_entity(new_obj)

    def get_by_email(self, email: str) -> Optional[User]:
        obj = self.session.query(UserORM).filter_by(email=email).first()
        return self._to_entity(obj) if obj else None

    def get_by_id(self, user_id: int) -> Optional[User]:
        obj = self.session.get(UserORM, user_id)
        return self._to_entity(obj) if obj else None

    def _to_entity(self, orm: UserORM) -> User:
        """Convierte un objeto ORM de SQLAlchemy a una Entidad de Dominio User."""
        return User(
            id=cast(Any, orm.id),
            email=cast(Any, orm.email),
            hashed_password=cast(Any, orm.hashed_password),
            full_name=cast(Any, orm.full_name),
            is_active=cast(Any, orm.is_active),
            is_admin=cast(Any, orm.is_admin)
        )
