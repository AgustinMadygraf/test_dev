"""
Path: tests/test_adaptadores.py
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock

from src.adaptadores.controladores.expediente_controller import ExpedienteController
from src.adaptadores.pasarelas.expediente_gateway import ExpedienteGateway
from src.adaptadores.presentadores.expediente_presenter import ExpedientePresenter
from src.aplicacion.expediente import ExpedienteUseCases
from src.dominio.entidades.expediente import EstadoExpediente, Expediente


def test_presenter_formats_expediente():
    presenter = ExpedientePresenter()
    expediente = Expediente(
        numero="123",
        extracto="Resumen",
        id_propietario=1,
        descripcion=None,
        estado=EstadoExpediente.BORRADOR,
        fecha_creacion=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
        ultima_modificacion=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    )

    formatted = presenter.format(expediente)

    assert formatted["numero_referencia"] == "123"
    assert formatted["resumen"] == "RESUMEN"
    assert formatted["id_propietario"] == 1
    assert formatted["descripcion_detallada"] == "Sin descripción"
    assert formatted["estado_actual"] == "Borrador"
    assert formatted["es_editable"] is True


def test_presenter_formats_list():
    presenter = ExpedientePresenter()
    exp1 = Expediente(numero="123", extracto="Uno", id_propietario=1)
    exp2 = Expediente(numero="456", extracto="Dos", id_propietario=1, descripcion="Desc")
    formatted = presenter.format_list([exp1, exp2])

    assert len(formatted) == 2
    assert formatted[0]["numero_referencia"] == "123"
    assert formatted[1]["descripcion_detallada"] == "Desc"


def test_expediente_controller_crear():
    use_cases = MagicMock(spec=ExpedienteUseCases)
    presenter = ExpedientePresenter()
    controller = ExpedienteController(use_cases, presenter)
    expediente = Expediente(numero="123", extracto="Test", id_propietario=1)
    use_cases.crear_expediente.return_value = expediente

    result = controller.crear({
        "numero": "123",
        "extracto": "Test",
        "id_propietario": 1,
        "descripcion": None
    })

    assert result["numero_referencia"] == "123"
    use_cases.crear_expediente.assert_called_once_with(
        numero="123",
        extracto="Test",
        id_propietario=1,
        descripcion=None
    )


def test_expediente_controller_listar():
    use_cases = MagicMock(spec=ExpedienteUseCases)
    presenter = ExpedientePresenter()
    controller = ExpedienteController(use_cases, presenter)
    expediente = Expediente(numero="123", extracto="Test", id_propietario=1)
    use_cases.listar_expedientes.return_value = [expediente]

    result = controller.listar()

    assert isinstance(result, list)
    assert result[0]["numero_referencia"] == "123"
    use_cases.listar_expedientes.assert_called_once()


def test_expediente_controller_obtener_no_encontrado():
    use_cases = MagicMock(spec=ExpedienteUseCases)
    presenter = ExpedientePresenter()
    controller = ExpedienteController(use_cases, presenter)
    use_cases.obtener_expediente.return_value = None

    result = controller.obtener(1)

    assert result is None


def test_expediente_gateway_guardar_y_buscar_todos_filtra_por_propietario():
    db_adapter = MagicMock()
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    db_adapter.save.return_value = {
        "id": 1,
        "numero": "123",
        "extracto": "Test",
        "id_propietario": 1,
        "descripcion": None,
        "estado": EstadoExpediente.BORRADOR,
        "fecha_creacion": now,
        "ultima_modificacion": now
    }
    db_adapter.find_all.return_value = [
        {
            "id": 1,
            "numero": "123",
            "extracto": "Test",
            "id_propietario": 1,
            "descripcion": None,
            "estado": EstadoExpediente.BORRADOR,
            "fecha_creacion": now,
            "ultima_modificacion": now
        },
        {
            "id": 2,
            "numero": "456",
            "extracto": "Otro",
            "id_propietario": 2,
            "descripcion": "Desc",
            "estado": EstadoExpediente.BORRADOR,
            "fecha_creacion": now,
            "ultima_modificacion": now
        }
    ]
    gateway = ExpedienteGateway(db_adapter)
    expediente = Expediente(numero="123", extracto="Test", id_propietario=1)

    persisted = gateway.guardar(expediente)
    assert persisted.id == 1
    assert str(persisted.numero) == "123"
    assert db_adapter.save.called

    results = gateway.buscar_todos(id_propietario=1)
    assert len(results) == 1
    assert results[0].id_propietario == 1
