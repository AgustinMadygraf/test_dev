# Path: tests/test_adaptadores.py

from datetime import datetime, timezone
from unittest.mock import MagicMock

from src.adaptadores.controladores.expediente_controller import ControladorExpediente
from src.adaptadores.pasarelas.expediente_gateway import PasarelaExpediente
from src.adaptadores.presentadores.expediente_presenter import PresentadorExpediente
from src.aplicacion.expediente import CasosUsoExpediente
from src.dominio.entidades.expediente import EstadoExpediente, Expediente
from src.dominio.objetos_valor import NumeroExpediente

def test_presenter_formats_expediente():
    presentador = PresentadorExpediente()
    expediente = Expediente(
        numero=NumeroExpediente("123"),
        extracto="Resumen",
        id_propietario=1,
        descripcion=None,
        estado=EstadoExpediente.BORRADOR,
        fecha_creacion=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
        ultima_modificacion=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    )

    formateado = presentador.formatear(expediente)

    assert formateado["numero_referencia"] == "123"
    assert formateado["resumen"] == "RESUMEN"
    assert formateado["id_propietario"] == 1
    assert formateado["descripcion_detallada"] == "Sin descripción"
    assert formateado["estado_actual"] == "Borrador"
    assert formateado["es_editable"] is True


def test_presenter_formats_list():
    presentador = PresentadorExpediente()
    exp1 = Expediente(numero=NumeroExpediente("123"), extracto="Uno", id_propietario=1)
    exp2 = Expediente(numero=NumeroExpediente("456"), extracto="Dos", id_propietario=1, descripcion="Desc")
    formateado = presentador.formatear_lista([exp1, exp2])

    assert len(formateado) == 2
    assert formateado[0]["numero_referencia"] == "123"
    assert formateado[1]["descripcion_detallada"] == "Desc"


def test_expediente_controller_crear():
    casos_uso = MagicMock(spec=CasosUsoExpediente)
    presentador = PresentadorExpediente()
    controlador = ControladorExpediente(casos_uso, presentador)
    expediente = Expediente(numero=NumeroExpediente("123"), extracto="Test", id_propietario=1)
    casos_uso.crear_expediente.return_value = expediente

    resultado = controlador.crear({
        "numero": "123",
        "extracto": "Test",
        "id_propietario": 1,
        "descripcion": None
    })

    assert resultado["numero_referencia"] == "123"
    casos_uso.crear_expediente.assert_called_once_with(
        numero="123",
        extracto="Test",
        id_propietario=1,
        descripcion=None
    )


def test_expediente_controller_listar():
    casos_uso = MagicMock(spec=CasosUsoExpediente)
    presentador = PresentadorExpediente()
    controlador = ControladorExpediente(casos_uso, presentador)
    expediente = Expediente(numero=NumeroExpediente("123"), extracto="Test", id_propietario=1)
    casos_uso.listar_expedientes.return_value = [expediente]

    resultado = controlador.listar()

    assert isinstance(resultado, list)
    assert resultado[0]["numero_referencia"] == "123"
    casos_uso.listar_expedientes.assert_called_once()


def test_expediente_controller_obtener_no_encontrado():
    casos_uso = MagicMock(spec=CasosUsoExpediente)
    presentador = PresentadorExpediente()
    controlador = ControladorExpediente(casos_uso, presentador)
    casos_uso.obtener_expediente.return_value = None

    resultado = controlador.obtener(1)

    assert resultado is None


def test_expediente_gateway_guardar_y_buscar_todos_filtra_por_propietario():
    # Este test no necesita cambios de nombres por ahora ya que prueba el gateway
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
        }
    ]
    
    gateway = PasarelaExpediente(db_adapter)
    expediente = Expediente(numero=NumeroExpediente("123"), extracto="Test", id_propietario=1)
    
    gateway.guardar(expediente)
    db_adapter.save.assert_called_once()
    
    resultados = gateway.buscar_todos(id_propietario=1)
    assert len(resultados) == 1
    assert str(resultados[0].numero) == "123"
