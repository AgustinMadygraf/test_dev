"""
Path: tests/test_use_cases.py
"""

import pytest
from unittest.mock import MagicMock
from src.dominio.entidades.expediente import Expediente
from src.dominio.excepciones import ErrorViolacionReglaNegocio

def test_register_user_success(auth_use_cases, mock_uow, mock_security, mock_user):
    # Arrange
    mock_uow.usuarios.buscar_por_correo.return_value = None
    mock_security.obtener_hash_contrasena.return_value = "contrasena_hash"
    mock_uow.usuarios.guardar.return_value = mock_user

    # Act
    result = auth_use_cases.register("test@example.com", "contrasena123", "Test Usuario")

    # Assert
    assert str(result.correo) == "test@example.com"
    mock_uow.usuarios.guardar.assert_called_once()

def test_register_user_already_exists(auth_use_cases, mock_uow, mock_user):
    mock_uow.usuarios.buscar_por_correo.return_value = mock_user
    
    with pytest.raises(ErrorViolacionReglaNegocio, match="El correo electrónico ya está registrado"):
        auth_use_cases.register("test@example.com", "contrasena", "Name")

def test_login_success(auth_use_cases, mock_uow, mock_security, mock_user):
    # Arrange
    mock_uow.usuarios.buscar_por_correo.return_value = mock_user
    mock_security.verificar_contrasena.return_value = True
    mock_security.crear_token_acceso.return_value = "fake-jwt-token"

    # Act
    result = auth_use_cases.login("test@example.com", "contrasena123")

    # Assert
    assert result["access_token"] == "fake-jwt-token"
    assert result["token_type"] == "bearer"

def test_login_invalid_credentials(auth_use_cases, mock_uow, mock_security, mock_user):
    mock_uow.usuarios.buscar_por_correo.return_value = mock_user
    mock_security.verificar_contrasena.return_value = False
    
    with pytest.raises(ErrorViolacionReglaNegocio, match="Credenciales inválidas"):
        auth_use_cases.login("test@example.com", "wrong_pass")

def test_login_inactive_user(auth_use_cases, mock_uow, mock_security, mock_user):
    mock_user.es_activo = False
    mock_uow.usuarios.buscar_por_correo.return_value = mock_user
    mock_security.verificar_contrasena.return_value = True
    
    with pytest.raises(ErrorViolacionReglaNegocio, match="Usuario inactivo"):
        auth_use_cases.login("test@example.com", "contrasena123")

def test_crear_expediente_success(expediente_use_cases, mock_uow):
    # Arrange
    mock_uow.expedientes.buscar_por_numero.return_value = None
    mock_exp = Expediente(id=1, numero="123", extracto="Test", id_propietario=1)
    mock_uow.expedientes.guardar.return_value = mock_exp

    # Act
    result = expediente_use_cases.crear_expediente("123", "Test", 1)

    # Assert
    assert str(result.numero) == "123"
    mock_uow.expedientes.guardar.assert_called_once()

def test_crear_expediente_already_exists(expediente_use_cases, mock_uow):
    # Arrange
    mock_uow.expedientes.buscar_por_numero.return_value = MagicMock(spec=Expediente)
    
    # Act & Assert
    with pytest.raises(ErrorViolacionReglaNegocio, match="ya existe"):
        expediente_use_cases.crear_expediente("123", "Test", 1)

def test_listar_expedientes(expediente_use_cases, mock_uow):
    # Arrange
    mock_uow.expedientes.buscar_todos.return_value = []

    # Act
    result = expediente_use_cases.listar_expedientes(id_propietario=1)

    # Assert
    assert isinstance(result, list)
    mock_uow.expedientes.buscar_todos.assert_called_with(id_propietario=1)

def test_obtener_expediente(expediente_use_cases, mock_uow):
    # Arrange
    mock_exp = MagicMock(spec=Expediente)
    mock_uow.expedientes.buscar_por_id.return_value = mock_exp
    
    # Act
    result = expediente_use_cases.obtener_expediente(1)
    
    # Assert
    assert result == mock_exp
