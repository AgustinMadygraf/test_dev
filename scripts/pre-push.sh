#!/bin/bash

# Navegar a la raíz del proyecto (un nivel arriba de scripts/)
cd "$(dirname "$0")/.."

echo "🚀 Iniciando validaciones pre-push..."

# 1. Validar entorno virtual
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Error: No se encontró el entorno virtual en .venv/. Por favor, créalo e instala las dependencias."
    exit 1
fi

# 2. Opcional: Validar linting/formato (Recomendado)
# echo "🎨 Comprobando formato y linting..."
# ruff check . || exit 1

# 3. Ejecutar tests Python con cobertura
echo "🧪 Ejecutando tests Python con cobertura (Umbral mínimo: 85%)..."
PYTHONPATH=. pytest --cov=src --cov-report=term-missing --cov-fail-under=85 tests/
if [ $? -ne 0 ]; then
    echo "❌ Error: Tests Python fallidos o cobertura insuficiente."
    exit 1
fi

echo "✅ Validaciones pre-push completadas correctamente."
