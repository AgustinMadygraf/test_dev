"""
Path: tests/conftest.py
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_uow, get_security_service, get_current_user
from src.domain.services.unit_of_work import IUnitOfWork
from src.domain.services.security import ISecurityService
from src.domain.services.repositories import IUserRepository, IExpedienteRepository
from src.use_cases.auth import AuthUseCases
from src.use_cases.expediente import ExpedienteUseCases

@pytest.fixture
def mock_uow():
    uow = MagicMock(spec=IUnitOfWork)
    uow.users = MagicMock(spec=IUserRepository)
    uow.expedientes = MagicMock(spec=IExpedienteRepository)
    # Simular el context manager
    uow.__enter__.return_value = uow
    return uow

@pytest.fixture
def mock_security():
    return MagicMock(spec=ISecurityService)

@pytest.fixture
def auth_use_cases(mock_uow, mock_security):
    return AuthUseCases(mock_uow, mock_security)

@pytest.fixture
def expediente_use_cases(mock_uow):
    return ExpedienteUseCases(mock_uow)

@pytest.fixture
def mock_user():
    from src.domain.entities.user import User
    return User(
        id=1,
        email="test@example.com",
        hashed_password="hashed_secret",
        full_name="Test User"
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