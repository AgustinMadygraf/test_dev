"""
Path: src/infrastructure/sqlalchemy/seed.py
"""

from passlib.context import CryptContext
from src.infrastructure.settings.config import settings
from src.infrastructure.settings.logger import get_logger
from src.infrastructure.sqlalchemy.database import init_db, SessionLocal
from src.infrastructure.sqlalchemy.models import UsuarioORM as User, ExpedienteORM as Expediente

logger = get_logger("db_seed", settings.LOG_LEVEL)

# Configuración de seguridad (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def run_seed():
    logger.info("Iniciando validación de base de datos y seeding...")
    
    init_db()
    
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.correo == settings.ADMIN_EMAIL).first()
        if not admin:
            logger.info(f"Creando usuario administrador: {settings.ADMIN_EMAIL}")
            hashed_pw = pwd_context.hash(settings.ADMIN_PASSWORD)
            admin = User(correo=settings.ADMIN_EMAIL, contrasena_hash=hashed_pw)
            db.add(admin)
            db.commit()
            db.refresh(admin)
            
            logger.info("Agregando expediente de prueba...")
            db.add(Expediente(
                numero="2024-INI-001",
                extracto="Expediente de prueba inicial",
                descripcion="Creado automáticamente por el sistema de seeding.",
                id_propietario=admin.id
            ))
            db.commit()
            logger.info("✅ Seeding completado con éxito.")
        else:
            logger.info("ℹ️ El administrador ya existe. Saltando seeding.")
    except Exception as e:
        logger.error(f"❌ Error durante el seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
