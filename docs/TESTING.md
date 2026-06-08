# 🧪 Guía de Testing y Calidad

El proyecto utiliza una estrategia de pruebas exhaustiva para garantizar la estabilidad de los procesos de negocio.

## Ejecución de Tests

Para correr todas las pruebas y generar un reporte de cobertura en consola:
```bash
./scripts/pre-push.sh
```

## Umbral de Cobertura
Se ha definido un umbral estricto del **85%**. Si la cobertura total es inferior, el script de validación fallará.

## Estructura de Pruebas
- **Unitarias:** Localizadas en `tests/test_use_cases.py`, prueban la lógica pura de negocio.
- **Integración:** Localizadas en `tests/test_api.py`, prueban los endpoints usando `TestClient`.
- **Infraestructura:** Localizadas en `tests/test_infraestructura.py`, prueban los adaptadores de base de datos y el Unit of Work.

## Hooks de Git
Se recomienda enlazar el script de pre-push para automatizar la revisión antes de subir código:
`ln -sf ../../scripts/pre-push.sh .git/hooks/pre-push`