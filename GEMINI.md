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
5. *Corrección de Arquitectura*: Decisión de mantener las entidades en `src/entities/` como clases puras de Python (sin dependencias externas) para desacoplar el dominio de la infraestructura.