#  Guía de Instalación con Docker

Este manual describe el proceso para levantar el Sistema de Gestión de Expedientes en un entorno contenedorizado, garantizando la persistencia y la carga inicial de datos.

## Configuración Inicial

1.  **Variables de Entorno:**
    Crea un archivo `.env` en la raíz del proyecto basándote en la siguiente estructura:
    ```bash
    SECRET_KEY=tu_clave_secreta
    ADMIN_EMAIL=tu_admin@email.com
    ADMIN_PASSWORD=tu_contraseña_segura
    ```

2.  **Construcción y Ejecución:**
    Para compilar el entorno, preparar las dependencias y levantar los servicios en un solo paso:
    ```bash
    docker compose up -d --build
    ```

## Carga de Datos (Seeding)
El sistema detectará automáticamente si la base de datos está vacía y procederá a crear el usuario administrador definido en el `.env`, junto con un set de datos de prueba para validación inmediata.

---
*Para desarrollo tradicional (sin contenedores), consulte el archivo `INSTALLING.md` en la raíz del proyecto.*