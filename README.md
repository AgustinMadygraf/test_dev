# Sistema de Gestión de Expedientes

Este proyecto es una aplicación web robusta para la gestión de expedientes, desarrollada siguiendo principios de **Arquitectura Limpia (Clean Architecture)** y **SOLID**. Permite a los usuarios registrarse, autenticarse de forma segura y gestionar sus propios expedientes de manera aislada.

## 🚀 Tecnologías Utilizadas

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **Base de Datos:** MySQL / SQLite (vía SQLAlchemy ORM)
- **Seguridad:** Autenticación JWT con `passlib` (bcrypt) y `python-jose`.
- **Frontend:** HTML5, CSS3 (Bootstrap 5) y JavaScript Vanilla.
- **Testing:** Pytest con `pytest-cov` para reportes de cobertura.

## 📚 Documentación Detallada

Para facilitar la navegación, la documentación se ha dividido según el perfil de interés:

1.  **Guía de Instalación para Desarrolladores**: Todo lo necesario para preparar el entorno de desarrollo y levantar el servidor.
2.  **Manual de Usuario Final**: Explicación paso a paso de cómo registrarse, loguearse y gestionar expedientes.
3.  **Guía de Testing y Calidad**: Detalles sobre la ejecución de pruebas, umbrales de cobertura y hooks de Git.

## ⚡ Inicio Rápido

Si ya tienes el entorno configurado, simplemente ejecuta:
```bash
./run.sh
```

---
*Desarrollado como parte de una evaluación técnica de Ingeniería de Software.*