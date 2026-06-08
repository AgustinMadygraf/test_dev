# Path: tests/test_dominio.py

import pytest
from src.dominio.objetos_valor import CorreoElectronico, NumeroExpediente
from src.dominio.entidades.expediente import Expediente, EstadoExpediente
from src.dominio.excepciones import ErrorValorInvalido, ErrorTransicionEstadoInvalida

def test_email_valido():
    email = CorreoElectronico("test@example.com")
    assert str(email) == "test@example.com"

def test_email_invalido():
    with pytest.raises(ErrorValorInvalido):
        CorreoElectronico("invalido")

def test_numero_expediente_valido():
    num = NumeroExpediente("EXP-123")
    assert str(num) == "EXP-123"

def test_numero_expediente_invalido():
    with pytest.raises(ErrorValorInvalido):
        NumeroExpediente("EXP 123!")

def test_crear_expediente_borrador():
    exp = Expediente.crear_nuevo("123", "Extracto", 1)
    assert exp.estado == EstadoExpediente.BORRADOR

def test_transicion_estado_valida():
    exp = Expediente.crear_nuevo("123", "Extracto", 1)
    exp.cambiar_estado(EstadoExpediente.EN_CURSO)
    assert exp.estado == EstadoExpediente.EN_CURSO

def test_transicion_estado_invalida_archivado():
    exp = Expediente.crear_nuevo("123", "Extracto", 1)
    exp.cambiar_estado(EstadoExpediente.ARCHIVADO)
    with pytest.raises(ErrorTransicionEstadoInvalida):
        exp.cambiar_estado(EstadoExpediente.EN_CURSO)

def test_transicion_estado_prohibida_finalizado_a_borrador():
    exp = Expediente.crear_nuevo("123", "Extracto", 1)
    exp.cambiar_estado(EstadoExpediente.FINALIZADO)
    with pytest.raises(ErrorTransicionEstadoInvalida):
        exp.cambiar_estado(EstadoExpediente.BORRADOR)
