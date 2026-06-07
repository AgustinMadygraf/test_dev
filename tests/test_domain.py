import pytest
from src.domain.value_objects import Email, NumeroExpediente
from src.domain.entities.expediente import Expediente, ExpedienteStatus
from src.domain.exceptions import InvalidValueError, InvalidStateTransitionError

def test_email_valido():
    email = Email("test@example.com")
    assert str(email) == "test@example.com"

def test_email_invalido():
    with pytest.raises(InvalidValueError):
        Email("invalido")

def test_numero_expediente_valido():
    num = NumeroExpediente("EXP-123")
    assert str(num) == "EXP-123"

def test_numero_expediente_invalido():
    with pytest.raises(InvalidValueError):
        NumeroExpediente("EXP 123!")

def test_crear_expediente_borrador():
    exp = Expediente.crear_nuevo("123", "Extracto", 1)
    assert exp.estado == ExpedienteStatus.BORRADOR

def test_transicion_estado_valida():
    exp = Expediente.crear_nuevo("123", "Extracto", 1)
    exp.cambiar_estado(ExpedienteStatus.EN_CURSO)
    assert exp.estado == ExpedienteStatus.EN_CURSO

def test_transicion_estado_invalida_archivado():
    exp = Expediente.crear_nuevo("123", "Extracto", 1)
    exp.cambiar_estado(ExpedienteStatus.ARCHIVADO)
    with pytest.raises(InvalidStateTransitionError):
        exp.cambiar_estado(ExpedienteStatus.EN_CURSO)

def test_transicion_estado_prohibida_finalizado_a_borrador():
    exp = Expediente.crear_nuevo("123", "Extracto", 1)
    exp.cambiar_estado(ExpedienteStatus.FINALIZADO)
    with pytest.raises(InvalidStateTransitionError):
        exp.cambiar_estado(ExpedienteStatus.BORRADOR)
