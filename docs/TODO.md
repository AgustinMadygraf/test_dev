# Task List - Gestión de Expedientes

## Fase 1: Entorno y Base de Datos
- [ ] Configurar `docker-compose.yml` con FastAPI y MySQL 8.0.
- [/] Configurar SQLAlchemy (Engine y Session) y Alembic para migraciones.
- [x] Definir Dominio: Entidades y Repositorios en `src/domain/`.

## Fase 2: Backend y Autenticación
- [ ] Implementar lógica de autenticación (Login).
- [x] Implementar Capa de Aplicación: Casos de Uso en `src/application/`.
- [ ] Desarrollar endpoints de la API en FastAPI.

## Fase 3: Frontend y Refinamiento
- [ ] Crear templates base con Jinja2 (Login y Home).
- [ ] Implementar interactividad básica con JavaScript en el Home.
- [ ] Escribir tests unitarios con `pytest` para los endpoints.
- [ ] Completar documentación técnica en `README.md`.