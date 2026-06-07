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

    def registrar(self, correo: str, contrasena: str, nombre_completo: Optional[str] = None) -> Usuario:
        with self.uow:
            correo_vo = correo if isinstance(correo, CorreoElectronico) else CorreoElectronico(correo)
            correo_str = correo_vo.direccion if hasattr(correo_vo, "direccion") else str(correo_vo)
            usuario_existente = self.uow.usuarios.buscar_por_correo(correo_str)
            if usuario_existente:
                raise ErrorViolacionReglaNegocio("El correo electrónico ya está registrado")

            contrasena_hash = self.servicio_seguridad.obtener_hash_contrasena(contrasena)

            nuevo_usuario = Usuario(
                correo=correo_vo,
                contrasena_hash=contrasena_hash,
                nombre_completo=nombre_completo,
            )
            usuario_creado = self.uow.usuarios.guardar(nuevo_usuario)
            return usuario_creado

    def iniciar_sesion(self, correo: str, contrasena: str) -> dict:
        with self.uow:
            correo_vo = correo if isinstance(correo, CorreoElectronico) else CorreoElectronico(correo)
            correo_str = correo_vo.direccion if hasattr(correo_vo, "direccion") else str(correo_vo)
            usuario = self.uow.usuarios.buscar_por_correo(correo_str)

            if not usuario or not self.servicio_seguridad.verificar_contrasena(contrasena, usuario.contrasena_hash):
                raise ErrorViolacionReglaNegocio("Credenciales inválidas")

            if not usuario.es_activo:
                raise ErrorViolacionReglaNegocio("Usuario inactivo")

            correo_str = usuario.correo.direccion if hasattr(usuario.correo, "direccion") else usuario.correo
            token_acceso = self.servicio_seguridad.crear_token_acceso(datos={"sub": str(correo_str)})
            return {"access_token": token_acceso, "token_type": "bearer"}
