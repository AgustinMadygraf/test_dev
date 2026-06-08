# Path: src/aplicacion/auth.py

from typing import Optional
from src.dominio.objetos_valor import CorreoElectronico
from src.dominio.entidades.usuario import Usuario
from src.aplicacion.servicios.unidad_de_trabajo import UnidadDeTrabajo
from src.aplicacion.servicios.seguridad import IServicioSeguridad
from src.dominio.excepciones import ErrorViolacionReglaNegocio

class CasosUsoAutenticacion:
    def __init__(self, uow: UnidadDeTrabajo, servicio_seguridad: IServicioSeguridad):
        self.uow = uow
        self.servicio_seguridad = servicio_seguridad

    def registrar(self, correo: CorreoElectronico, contrasena: str, nombre_completo: Optional[str] = None) -> Usuario:
        with self.uow:
            usuario_existente = self.uow.usuarios.buscar_por_correo(correo.direccion)
            if usuario_existente:
                raise ErrorViolacionReglaNegocio("El correo electrónico ya está registrado")

            contrasena_hash = self.servicio_seguridad.obtener_hash_contrasena(contrasena)

            nuevo_usuario = Usuario(
                correo=correo,
                contrasena_hash=contrasena_hash,
                nombre_completo=nombre_completo,
            )
            usuario_creado = self.uow.usuarios.guardar(nuevo_usuario)
            return usuario_creado

    def iniciar_sesion(self, correo: CorreoElectronico, contrasena: str) -> dict:
        with self.uow:
            usuario = self.uow.usuarios.buscar_por_correo(correo.direccion)

            if not usuario or not self.servicio_seguridad.verificar_contrasena(contrasena, usuario.contrasena_hash):
                raise ErrorViolacionReglaNegocio("Credenciales inválidas")

            if not usuario.es_activo:
                raise ErrorViolacionReglaNegocio("Usuario inactivo")

            token_acceso = self.servicio_seguridad.crear_token_acceso(datos={"sub": usuario.correo.direccion})
            return {"access_token": token_acceso, "token_type": "bearer"}
