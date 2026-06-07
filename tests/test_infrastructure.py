"""
Path: tests/test_infrastructure.py
"""

import pytest
from unittest.mock import MagicMock
from src.infrastructure.sqlalchemy.adapter import SQLAlchemyDatabaseAdapter, SQLAlchemyUserAdapter
from src.infrastructure.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from src.domain.entities.expediente import Expediente
from src.infrastructure.sqlalchemy.models import ExpedienteORM, UserORM
from src.domain.entities.user import User

def test_database_adapter_get_all(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    mock_session.query.return_value.all.return_value = []
    
    results = adapter.get_all()
    assert results == []
    mock_session.query.assert_called()

def test_database_adapter_get_by_numero(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    result = adapter.get_by_numero("123")
    assert result is None

def test_database_adapter_save_new(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    exp = Expediente(numero="2023-X", extracto="Test", owner_id=1)
    
    # Simular el refresco de la base de datos asignando un ID
    def mock_refresh(obj):
        obj.id = 1
    mock_session.refresh.side_effect = mock_refresh

    result = adapter.save(exp)
    assert result.id == 1
    mock_session.add.assert_called_once()

def test_database_adapter_save_update(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    # Mockeamos session.get para devolver un objeto ORM existente
    mock_orm = ExpedienteORM(id=1, numero="OLD", extracto="Old", owner_id=1)
    mock_session.get.return_value = mock_orm
    
    exp = Expediente(id=1, numero="NEW", extracto="New", owner_id=1)
    result = adapter.save(exp)
    
    assert str(result.numero) == "NEW"
    mock_session.flush.assert_called_once()

def test_database_adapter_get_by_id(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    mock_session.get.return_value = None
    assert adapter.get_by_id(1) is None

def test_user_adapter_get_by_email(mock_session):
    adapter = SQLAlchemyUserAdapter(mock_session)
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    result = adapter.get_by_email("test@test.com")
    assert result is None

def test_user_adapter_save_new(mock_session):
    adapter = SQLAlchemyUserAdapter(mock_session)
    user = User(email="test@test.com", hashed_password="pw")
    
    def mock_refresh(obj):
        obj.id = 1
    mock_session.refresh.side_effect = mock_refresh
    
    result = adapter.save(user)
    assert result.id == 1
    mock_session.add.assert_called_once()

def test_uow_automatic_commit(mock_session):
    session_factory = MagicMock(return_value=mock_session)
    uow = SQLAlchemyUnitOfWork(session_factory)
    
    # Al salir del bloque sin excepción, IUnitOfWork llama a commit()
    with uow:
        pass
    mock_session.commit.assert_called_once()

def test_uow_manual_rollback(mock_session):
    session_factory = MagicMock(return_value=mock_session)
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.rollback()
    mock_session.rollback.assert_called_once()

def test_uow_rollback_on_exception(mock_session):
    session_factory = MagicMock(return_value=mock_session)
    uow = SQLAlchemyUnitOfWork(session_factory)
    
    with pytest.raises(Exception):
        with uow:
            raise Exception("DB Error")
    mock_session.rollback.assert_called()