"""
Path: tests/test_infrastructure.py
"""

import pytest
from unittest.mock import MagicMock
from src.infrastructure.sqlalchemy.adapter import SQLAlchemyDatabaseAdapter, SQLAlchemyUsuarioAdapter
from src.infrastructure.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from src.dominio.entidades.expediente import Expediente
from src.infrastructure.sqlalchemy.models import ExpedienteORM, UsuarioORM
from src.dominio.entidades.usuario import Usuario

def test_database_adapter_buscar_todos(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    mock_session.query.return_value.all.return_value = []
    
    results = adapter.buscar_todos()
    assert results == []
    mock_session.query.assert_called()

def test_database_adapter_buscar_por_numero(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    result = adapter.buscar_por_numero("123")
    assert result is None

def test_database_adapter_guardar_new(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    exp = Expediente(numero="2023-X", extracto="Test", id_propietario=1)
    
    # Simular el refresco de la base de datos asignando un ID
    def mock_refresh(obj):
        obj.id = 1
    mock_session.refresh.side_effect = mock_refresh

    result = adapter.guardar(exp)
    assert result.id == 1
    mock_session.add.assert_called_once()

def test_database_adapter_guardar_update(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    # Mockeamos session.get para devolver un objeto ORM existente
    mock_orm = ExpedienteORM(id=1, numero="OLD", extracto="Old", id_propietario=1)
    mock_session.get.return_value = mock_orm
    
    exp = Expediente(id=1, numero="NEW", extracto="New", id_propietario=1)
    result = adapter.guardar(exp)
    
    assert str(result.numero) == "NEW"
    mock_session.flush.assert_called_once()

def test_database_adapter_buscar_por_id(mock_session):
    adapter = SQLAlchemyDatabaseAdapter(mock_session)
    mock_session.get.return_value = None
    assert adapter.buscar_por_id(1) is None

def test_user_adapter_buscar_por_correo(mock_session):
    adapter = SQLAlchemyUsuarioAdapter(mock_session)
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    result = adapter.buscar_por_correo("test@test.com")
    assert result is None

def test_user_adapter_guardar_new(mock_session):
    adapter = SQLAlchemyUsuarioAdapter(mock_session)
    user = Usuario(correo="test@test.com", contrasena_hash="pw")
    
    def mock_refresh(obj):
        obj.id = 1
    mock_session.refresh.side_effect = mock_refresh
    
    result = adapter.guardar(user)
    assert result.id == 1
    mock_session.add.assert_called_once()

def test_uow_automatic_confirmar(mock_session):
    session_factory = MagicMock(return_value=mock_session)
    uow = SQLAlchemyUnitOfWork(session_factory)
    
    # Al salir del bloque sin excepción, UnidadDeTrabajo llama a confirmar()
    with uow:
        pass
    mock_session.commit.assert_called_once()

def test_uow_manual_revertir(mock_session):
    session_factory = MagicMock(return_value=mock_session)
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.revertir()
    mock_session.rollback.assert_called_once()

def test_uow_rollback_on_exception(mock_session):
    session_factory = MagicMock(return_value=mock_session)
    uow = SQLAlchemyUnitOfWork(session_factory)
    
    with pytest.raises(Exception):
        with uow:
            raise Exception("DB Error")
    mock_session.rollback.assert_called()