# Gemini Project Log

Registro de decisiones y prompts clave utilizados durante el desarrollo.

## Decisiones Técnicas
- **Entidad Elegida**: Expedientes (Domain: Legal/Administrativo).
- **Stack**: FastAPI + SQLAlchemy + MySQL (definido por el usuario).

## Historial de Prompts Críticos
1. *Revisión inicial de requerimientos*: Enumeración de certezas y dudas.
2. *Definición de dominio*: Selección de "Gestión de Expedientes" como eje central.
3. *Estructuración de documentos*: Creación de SRS, TODO, AGENT y GEMINI docs.
4. *Brainstorming de Negocio*: Propuesta de estados de expediente, roles de usuario y estructura modular.
5. *Entidades Puras*: Implementación de `User` y `Expediente` usando `dataclasses` para cumplir con Clean Architecture.
6. *Capa de Aplicación*: Creación de `IExpedienteRepository` y `ExpedienteUseCases` para desacoplar la lógica de la infraestructura.
7. *Refactor de Carpetas*: Reorganización a `src/domain/` y `src/application/` para seguir estándares de Clean Architecture.
8. *Ajustes de Entorno*: Creación de archivos `__init__.py` y corrección de Optional typing para resolver errores de Pylance.
9. *Gestión de Dependencias*: Creación de `requirements.txt` y resolución de importaciones de infraestructura (SQLAlchemy).
10. *Infraestructura*: Configuración de conexión y sesión de base de datos en `src/infrastructure/database.py`.
11. *Contratos de Repositorio*: Definición de `IUserRepository` e `IExpedienteRepository` en la capa de dominio para inversión de dependencias.