# 🧪 Guía de Testing y Calidad

El proyecto tiene una estrategia de pruebas bastante completa para que el sistema no se rompa con los cambios.

## Ejecución de Tests

Para correr todas las pruebas y generar un reporte de cobertura en consola, ejecutá:
./scripts/pre-push.sh

## Umbral de Cobertura
Pedimos un umbral estricto del 85%. Si la cobertura total da menos, el script de validación te va a tirar error.

## Estructura de Pruebas
- **Unitarias:** En tests/test_aplicacion.py (o similar), prueban la lógica pura de negocio.
- **Integración:** En tests/test_api.py, prueban los endpoints usando TestClient.
- **Infraestructura:** En tests/test_infraestructura.py, prueban los adaptadores de base de datos y el Unit of Work.

## Hooks de Git
Te recomendamos enlazar el script de pre-push para automatizar la revisión antes de hacer push:
ln -sf ../../scripts/pre-push.sh .git/hooks/pre-push
