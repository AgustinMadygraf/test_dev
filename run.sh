#!/bin/bash

# Activar el entorno virtual
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Error: No se encontró el entorno virtual en .venv/"
    echo "Asegúrate de haberlo creado con: python3 -m venv .venv"
    exit 1
fi

# Ejecución de uvicorn apuntando a la instancia de la app
uvicorn src.infrastructure.fastapi.app:app --reload --host 127.0.0.1 --port 8000