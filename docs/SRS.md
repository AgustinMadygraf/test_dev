# Software Requirements Specification (SRS)

## 1. Introducción
El sistema tiene como objetivo centralizar la gestión de expedientes administrativos, permitiendo su registro y consulta mediante una interfaz web y una API REST.

## 2. Requerimientos Funcionales
- **RF01 - Autenticación**: El sistema debe permitir el ingreso de usuarios registrados.
- **RF02 - Registro de Expedientes**: Un usuario autenticado podrá crear un nuevo expediente con campos obligatorios (número, extracto, fecha).
- **RF03 - Consulta de Expedientes**: El sistema permitirá visualizar el listado de expedientes existentes.
- **RF04 - Interfaz de Usuario**: Se debe proveer un "Home" accesible tras el login que resuma la información principal.

## 3. Requerimientos No Funcionales
- **RNF01 - Persistencia**: Uso obligatorio de MySQL a través del ORM SQLAlchemy.
- **RNF02 - Portabilidad**: La aplicación debe ser ejecutable mediante contenedores Docker.
- **RNF03 - Calidad de Código**: Cobertura de tests para los endpoints principales.

## 4. Tecnologías
- **Backend**: FastAPI (Python).
- **Database**: MySQL.
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla).