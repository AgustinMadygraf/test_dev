# Path: src/dominio/excepciones.py

class ErrorDeDominio(Exception):
    pass

class ErrorViolacionReglaNegocio(ErrorDeDominio):
    pass

class ErrorTransicionEstadoInvalida(ErrorViolacionReglaNegocio):
    pass

class ErrorValorInvalido(ErrorDeDominio):
    pass
