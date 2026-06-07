from typing import Optional
from sqlalchemy.orm import sessionmaker, Session
from src.aplicacion.servicios.unidad_de_trabajo import UnidadDeTrabajo
from src.infrastructure.sqlalchemy.adapter import SQLAlchemyDatabaseAdapter, SQLAlchemyUsuarioAdapter

class SQLAlchemyUnitOfWork(UnidadDeTrabajo):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session: Optional[Session] = None

    def __enter__(self):
        self.session = self.session_factory()
        if self.session is None:
            raise RuntimeError("Failed to create a new SQLAlchemy session.")
        self.expedientes = SQLAlchemyDatabaseAdapter(self.session)
        self.usuarios = SQLAlchemyUsuarioAdapter(self.session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        if self.session:
            self.session.close()

    def confirmar(self):
        if not self.session:
            return
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def revertir(self):
        if self.session:
            self.session.rollback()
