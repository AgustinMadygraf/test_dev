# Dudas y Definiciones Pendientes

1. **Estrategia de Autenticación**: Dado que se requiere un "Home" con HTML, ¿se prefiere el uso de **OAuth2 con JWT** (estándar de FastAPI) o el manejo de **Sesiones basadas en Cookies** para facilitar la integración con el frontend?
2. **Arquitectura del Frontend**: ¿El frontend debe ser servido directamente por FastAPI mediante templates (Jinja2) o se espera una estructura de archivos estáticos totalmente independiente?
3. **Versión de MySQL**: ¿Existe alguna restricción o preferencia por una versión específica de MySQL (ej. 8.0) para la configuración de Docker?
4. **Alcance de la Lógica de Negocio**: Para los puntos extra, ¿hay algún flujo de permisos específico que se desee evaluar (ej. roles de admin/user)?