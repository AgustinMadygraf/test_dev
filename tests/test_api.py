"""
Path: tests/test_api.py
"""

import pytest
from src.domain.entidades.expediente import Expediente, EstadoExpediente
from unittest.mock import MagicMock

def test_read_main(client):
    response = client.get("/")
    # Si el index.html existe devuelve 200, sino el mensaje de API running
    assert response.status_code in [200, 404] 

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Service is running"}

def test_favicon(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 204

def test_read_login(client):
    response = client.get("/login")
    assert response.status_code in [200, 404]

def test_read_register(client):
    response = client.get("/register")
    assert response.status_code in [200, 404]

def test_api_crear_expediente(client, mock_uow):
    # Arrange
    mock_uow.expedientes.buscar_por_numero.return_value = None
    mock_uow.expedientes.guardar.return_value = Expediente(
        id=1, numero="2023-001", extracto="Test API", id_propietario=1,
        estado=EstadoExpediente.BORRADOR
    )

    # Act
    response = client.post("/expedientes/", json={
        "numero": "2023-001",
        "extracto": "Test API",
        "descripcion": "Una descripción"
    })

    # Assert
    assert response.status_code == 201
    assert response.json()["numero"] == "2023-001"

def test_api_crear_expediente_already_exists(client, mock_uow):
    mock_uow.expedientes.buscar_por_numero.return_value = MagicMock()
    response = client.post("/expedientes/", json={
        "numero": "EXISTE",
        "extracto": "Test"
    })
    assert response.status_code == 400

def test_api_listar_expedientes(client, mock_uow):
    mock_uow.expedientes.buscar_todos.return_value = []
    response = client.get("/expedientes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_api_obtener_expediente_owner(client, mock_uow, mock_user):
    mock_exp = Expediente(id=1, numero="123", extracto="Ex", id_propietario=mock_user.id)
    mock_uow.expedientes.buscar_por_id.return_value = mock_exp
    
    response = client.get("/expedientes/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_api_obtener_expediente_not_found(client, mock_uow):
    mock_uow.expedientes.buscar_por_id.return_value = None
    response = client.get("/expedientes/999")
    assert response.status_code == 404

def test_api_obtener_expediente_forbidden(client, mock_uow):
    # Expediente que pertenece a otro usuario (ID 99)
    mock_exp = Expediente(id=1, numero="123", extracto="Ex", id_propietario=99)
    mock_uow.expedientes.buscar_por_id.return_value = mock_exp
    
    response = client.get("/expedientes/1")
    assert response.status_code == 403
    assert "No tiene permisos" in response.json()["detail"]

def test_auth_login_api(client, mock_uow, mock_security, mock_user):
    # Arrange
    mock_uow.usuarios.buscar_por_correo.return_value = mock_user
    mock_security.verificar_contrasena.return_value = True
    mock_security.crear_token_acceso.return_value = "fake-token"
    
    # Act
    response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    
    # Assert
    assert response.status_code == 200
    assert response.json()["access_token"] == "fake-token"

def test_auth_login_api_failure(client, mock_uow, mock_security):
    mock_uow.usuarios.buscar_por_correo.return_value = None
    response = client.post("/auth/login", data={"username": "not@found.com", "password": "any"})
    assert response.status_code == 400

def test_auth_register_api_failure(client, mock_uow):
    mock_uow.usuarios.buscar_por_correo.return_value = MagicMock()
    response = client.post("/auth/register", json={"correo": "exists@test.com", "contrasena": "any"})
    assert response.status_code == 400

