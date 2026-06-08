"""
Path: tests/conftest.py
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.infraestructura.fastapi.app import app
from src.infraestructura.fastapi.dependencies import get_uow, get_security_service, get_current_user
from src.aplicacion.servicios.unidad_de_trabajo import UnidadDeTrabajo
from src.aplicacion.servicios.seguridad import IServicioSeguridad
from src.dominio.servicios.repositorios import IRepositorioUsuario, IRepositorioExpediente
from src.aplicacion.auth import CasosUsoAutenticacion
from src.aplicacion.expediente import CasosUsoExpediente

@pytest.fixture
def mock_uow():
    uow = MagicMock(spec=UnidadDeTrabajo)
    uow.usuarios = MagicMock(spec=IRepositorioUsuario)
    uow.expedientes = MagicMock(spec=IRepositorioExpediente)
    # Simular el context manager
    uow.__enter__.return_value = uow
    return uow

@pytest.fixture
def mock_security():
    return MagicMock(spec=IServicioSeguridad)

@pytest.fixture
def auth_use_cases(mock_uow, mock_security):
    return CasosUsoAutenticacion(mock_uow, mock_security)

@pytest.fixture
def expediente_use_cases(mock_uow):
    return CasosUsoExpediente(mock_uow)

@pytest.fixture
def mock_user():
    from src.dominio.entidades.usuario import Usuario
    return Usuario(
        id=1,
        correo="test@example.com",
        contrasena_hash="hashed_secret",
        nombre_completo="Test Usuario"
    )

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def client(mock_uow, mock_security, mock_user):
    # Overrides de dependencias para FastAPI
    app.dependency_overrides[get_uow] = lambda: mock_uow
    app.dependency_overrides[get_security_service] = lambda: mock_security
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()

@pytest.fixture
def client_unauthenticated():
    # Cliente sin el override de get_current_user para probar errores 401
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()