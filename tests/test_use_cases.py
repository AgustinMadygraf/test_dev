"""
Path: tests/test_use_cases.py
"""

import pytest
from unittest.mock import MagicMock
from src.domain.entities.expediente import Expediente

def test_register_user_success(auth_use_cases, mock_uow, mock_security, mock_user):
    # Arrange
    mock_uow.users.get_by_email.return_value = None
    mock_security.get_password_hash.return_value = "hashed_password"
    mock_uow.users.save.return_value = mock_user

    # Act
    result = auth_use_cases.register("test@example.com", "password123", "Test User")

    # Assert
    assert result.email == "test@example.com"
    mock_uow.users.save.assert_called_once()

def test_register_user_already_exists(auth_use_cases, mock_uow, mock_user):
    mock_uow.users.get_by_email.return_value = mock_user
    
    with pytest.raises(ValueError, match="El correo electrónico ya está registrado"):
        auth_use_cases.register("test@example.com", "password", "Name")

def test_login_success(auth_use_cases, mock_uow, mock_security, mock_user):
    # Arrange
    mock_uow.users.get_by_email.return_value = mock_user
    mock_security.verify_password.return_value = True
    mock_security.create_access_token.return_value = "fake-jwt-token"

    # Act
    result = auth_use_cases.login("test@example.com", "password123")

    # Assert
    assert result["access_token"] == "fake-jwt-token"
    assert result["token_type"] == "bearer"

def test_login_invalid_credentials(auth_use_cases, mock_uow, mock_security, mock_user):
    mock_uow.users.get_by_email.return_value = mock_user
    mock_security.verify_password.return_value = False
    
    with pytest.raises(ValueError, match="Credenciales inválidas"):
        auth_use_cases.login("test@example.com", "wrong_pass")

def test_login_inactive_user(auth_use_cases, mock_uow, mock_security, mock_user):
    mock_user.is_active = False
    mock_uow.users.get_by_email.return_value = mock_user
    mock_security.verify_password.return_value = True
    
    with pytest.raises(ValueError, match="Usuario inactivo"):
        auth_use_cases.login("test@example.com", "password123")

def test_crear_expediente_success(expediente_use_cases, mock_uow):
    # Arrange
    mock_uow.expedientes.get_by_numero.return_value = None
    mock_exp = Expediente(id=1, numero="123", extracto="Test", owner_id=1)
    mock_uow.expedientes.save.return_value = mock_exp

    # Act
    result = expediente_use_cases.crear_expediente("123", "Test", 1)

    # Assert
    assert result.numero == "123"
    mock_uow.expedientes.save.assert_called_once()

def test_crear_expediente_already_exists(expediente_use_cases, mock_uow):
    # Arrange
    mock_uow.expedientes.get_by_numero.return_value = MagicMock(spec=Expediente)
    
    # Act & Assert
    with pytest.raises(ValueError, match="ya existe"):
        expediente_use_cases.crear_expediente("123", "Test", 1)

def test_listar_expedientes(expediente_use_cases, mock_uow):
    # Arrange
    mock_uow.expedientes.get_all.return_value = []

    # Act
    result = expediente_use_cases.listar_expedientes(owner_id=1)

    # Assert
    assert isinstance(result, list)
    mock_uow.expedientes.get_all.assert_called_with(owner_id=1)

def test_obtener_expediente(expediente_use_cases, mock_uow):
    # Arrange
    mock_exp = MagicMock(spec=Expediente)
    mock_uow.expedientes.get_by_id.return_value = mock_exp
    
    # Act
    result = expediente_use_cases.obtener_expediente(1)
    
    # Assert
    assert result == mock_exp