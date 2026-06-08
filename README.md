# Sistema de Gestión de Expedientes

Este proyecto es una aplicación web para la gestión de expedientes. Te permite registrarte, loguearte de forma segura y gestionar tus propios expedientes de manera aislada.

## 🚀 Tecnologías que usamos

- **Backend:** FastAPI (Python 3.12+)
- **Base de Datos:** SQLite (vía SQLAlchemy ORM)
- **Seguridad:** Autenticación JWT.
- **Frontend:** HTML5, CSS3 (Bootstrap 5) y JavaScript Vanilla.
- **Testing:** Pytest con pytest-cov.

## 📚 Documentación

Acá tenés toda la info para entender y manejar el proyecto:

1.  **Guía de Instalación**: Ver docs/INSTALLING.md para configurar el entorno.
2.  **Manual de Usuario**: Ver docs/USER_GUIDE.md para aprender a usar el sistema.
3.  **Guía de Testing**: Ver docs/TESTING.md para detalles sobre cómo corremos las pruebas y mantenemos la calidad.
4.  **Documentación de API**: Una vez corriendo el servidor, entrá a http://localhost:8000/docs para ver la especificación OpenAPI interactiva.

## ⚡ Inicio Rápido

### Desarrollo Local (sin Docker)
Prepará tu entorno virtual y ejecutá:
./run.sh

### Entorno Contenedorizado (Docker)
Asegurate de copiar .env.example a .env y configurar tus variables antes de ejecutar:
docker compose up -d --build
