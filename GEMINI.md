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
12. *Implementación de Interfaces*: Implementación del método `get_by_id` en `ExpedienteGateway` y adición de firma `find_by_id` en el protocolo `DatabaseAdapter`.
13. *Infraestructura y Cableado de Clean Architecture*: Creación de un `InMemoryDatabaseAdapter` como adaptador concreto provisional y refactorización del endpoint de FastAPI en `app.py` y de los esquemas de respuesta en `schemas.py` para utilizar todo el flujo Clean Architecture (Gateway -> Entidad -> Presenter) de forma desacoplada.
14. *Refactor del Presenter*: Inyección del `ExpedientePresenter` en el `ExpedienteController` para cumplir rigurosamente con la separación de capas en Clean Architecture, evitando que el punto de entrada de FastAPI deba orquestar el formateo de datos.