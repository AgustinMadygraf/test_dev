# Path: tests/test_seed.py

from unittest.mock import MagicMock, patch
from src.infraestructura.sqlalchemy.seed import run_seed

def test_run_seed_admin_already_exists():
    with patch('src.infraestructura.sqlalchemy.seed.SessionLocal') as mock_session_factory,          patch('src.infraestructura.sqlalchemy.seed.logger') as mock_logger:
        
        mock_db = MagicMock()
        mock_session_factory.return_value = mock_db
        
        # Simular que el admin ya existe
        mock_admin = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_admin
        
        run_seed()
        
        mock_db.add.assert_not_called()
        mock_logger.info.assert_any_call("ℹ️ El administrador ya existe. Saltando seeding.")

def test_run_seed_creates_new_admin():
    with patch('src.infraestructura.sqlalchemy.seed.SessionLocal') as mock_session_factory,          patch('src.infraestructura.sqlalchemy.seed.init_db'),          patch('src.infraestructura.sqlalchemy.seed.logger'):
        
        mock_db = MagicMock()
        mock_session_factory.return_value = mock_db
        
        # Simular que el admin NO existe
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        run_seed()
        
        assert mock_db.add.called
        assert mock_db.commit.called
