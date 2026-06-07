FROM python:3.12-slim

# Evitar que Python genere archivos .pyc y asegurar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalación de dependencias de sistema mínimas si fuera necesario
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# El frontend se copia en el contenedor junto con el resto del proyecto.
# FastAPI sirve estos archivos desde /app/frontend.

# Crear carpeta para la base de datos SQLite y asignar permisos
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["sh", "-c", "python -m src.infrastructure.sqlalchemy.seed && uvicorn src.infrastructure.fastapi.app:app --host 0.0.0.0 --port 8000"]