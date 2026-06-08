# Guía de Instalación con Docker

Acá te explicamos cómo levantar el Sistema de Gestión de Expedientes en un entorno contenedorizado, para que tengas la persistencia y la carga inicial de datos lista de una.

## Configuración Inicial

1.  **Variables de Entorno:**
    Creá un archivo .env en la raíz del proyecto basándote en .env.example:
    SECRET_KEY=tu_clave_secreta
    ADMIN_EMAIL=tu_admin@email.com
    ADMIN_PASSWORD=tu_contraseña_segura

2.  **Construcción y Ejecución:**
    Para compilar el entorno, preparar las dependencias y levantar los servicios de un saque:
    docker compose up -d --build

## Carga de Datos (Seeding)
El sistema detecta automáticamente si la base de datos está vacía y crea el usuario administrador que definiste en el .env, junto con un par de datos de prueba para que puedas empezar a probar enseguida.
