#!/bin/bash

PORT=${HOST_PORT:-8000}

# Cerrar procesos locales que usen el puerto
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "El puerto $PORT ya está en uso por un proceso local. Cerrando proceso..."
    lsof -ti:$PORT | xargs kill -9
    sleep 1
fi

# Cerrar contenedores de Docker que usen el puerto
if command -v docker &> /dev/null; then
    CONTAINER_ID=$(docker ps --filter "publish=$PORT" -q)
    if [ ! -z "$CONTAINER_ID" ]; then
        echo "El puerto $PORT está siendo usado por un contenedor Docker ($CONTAINER_ID). Deteniendo contenedor..."
        docker stop $CONTAINER_ID
        sleep 1
    fi
fi

# Activar el entorno virtual
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Error: No se encontró el entorno virtual en .venv/"
    echo "Asegúrate de haberlo creado con: python3 -m venv .venv"
    exit 1
fi

# Ejecución de uvicorn apuntando a la instancia de la app
# Inicializar base de datos y seeding
python -m src.infrastructure.sqlalchemy.seed

uvicorn src.infrastructure.fastapi.app:app --reload --host 127.0.0.1 --port $PORT
