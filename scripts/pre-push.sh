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
# Si usas ruff o flake8, podrías descomentar las siguientes líneas:
# echo "🎨 Comprobando formato y linting..."
# ruff check . || exit 1

# 3. Ejecutar tests con cobertura
echo "🧪 Ejecutando tests con cobertura (Umbral mínimo: 85%)..."

# --cov=src: Indica qué carpeta medir
# --cov-report=term-missing: Muestra qué líneas exactas no están testeadas
# --cov-fail-under=85: Hace que el comando falle si no se llega al porcentaje
PYTHONPATH=. pytest --cov=src --cov-report=term-missing --cov-fail-under=85 tests/

if [ $? -eq 0 ]; then
    echo "✅ Calidad aprobada. Procediendo con el push."
else
    echo "❌ Error: La cobertura de tests es inferior al 85% o hay tests fallidos."
    exit 1
fi