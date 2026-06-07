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

# 3. Ejecutar tests Python con cobertura
echo "🧪 Ejecutando tests Python con cobertura (Umbral mínimo: 85%)..."
PYTHONPATH=. pytest --cov=src --cov-report=term-missing --cov-fail-under=85 tests/
if [ $? -ne 0 ]; then
    echo "❌ Error: Tests Python fallidos o cobertura insuficiente."
    exit 1
fi

# 4. Ejecutar tests frontend si existe carpeta frontend
if [ -d "frontend" ]; then
    echo "🧩 Ejecutando tests frontend (Jest)..."
    if ! command -v npm >/dev/null 2>&1; then
        echo "⚠️  npm no está disponible. Omisión de tests frontend."
    else
        pushd frontend >/dev/null || exit 1
        if [ -d node_modules ]; then
            npm test --silent || { echo "❌ Tests frontend fallidos."; popd >/dev/null; exit 1; }
        else
            npm ci --no-audit --no-fund || { echo "❌ Falló npm ci."; popd >/dev/null; exit 1; }
            npm test --silent || { echo "❌ Tests frontend fallidos."; popd >/dev/null; exit 1; }
        fi
        popd >/dev/null
    fi
fi

echo "✅ Validaciones pre-push completadas correctamente."
