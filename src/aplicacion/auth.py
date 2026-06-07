from src.dominio.objetos_valor import CorreoElectronico
from typing import Optional
from src.dominio.entidades.usuario import Usuario
from src.aplicacion.servicios.unidad_de_trabajo import IUnidadDeTrabajo
from src.aplicacion.servicios.seguridad import IServicioSeguridad
from src.dominio.excepciones import ErrorViolacionReglaNegocio

class AuthUseCases:
    def __init__(self, uow: IUnidadDeTrabajo, security_service: IServicioSeguridad):
        self.uow = uow
        self.security_service = security_service

    def register(self, correo: str, contrasena: str, nombre_completo: Optional[str] = None) -> Usuario:
        with self.uow:
            # 1. Verificar si el usuario ya existe
            correo_vo = correo if isinstance(correo, CorreoElectronico) else CorreoElectronico(correo)
            correo_str = correo_vo.direccion if hasattr(correo_vo, 'direccion') else str(correo_vo)
            existing_user = self.uow.usuarios.buscar_por_correo(correo_str)
            if existing_user:
                raise ErrorViolacionReglaNegocio("El correo electrónico ya está registrado")

            # 2. Hashear la contraseña (Infrastructura vía Abstracción)
            contrasena_hash = self.security_service.obtener_hash_contrasena(contrasena)

            # 3. Crear entidad y persistir
            # El objeto Usuario validará el correo internamente
            new_user = Usuario(correo=correo_vo, contrasena_hash=contrasena_hash, nombre_completo=nombre_completo)
            created_user = self.uow.usuarios.guardar(new_user)
            return created_user

    def login(self, correo: str, password: str) -> dict:
        with self.uow:
            correo_vo = correo if isinstance(correo, CorreoElectronico) else CorreoElectronico(correo)
            correo_str = correo_vo.direccion if hasattr(correo_vo, 'direccion') else str(correo_vo)
            user = self.uow.usuarios.buscar_por_correo(correo_str)
            
            if not user or not self.security_service.verificar_contrasena(password, user.contrasena_hash):
                raise ErrorViolacionReglaNegocio("Credenciales inválidas")
            
            if not user.es_activo:
                raise ErrorViolacionReglaNegocio("Usuario inactivo")
            
            # Usar direccion si correo es un Value Object
            correo_str = user.correo.direccion if hasattr(user.correo, 'direccion') else user.correo
            access_token = self.security_service.crear_token_acceso(datos={"sub": str(correo_str)})
            return {"access_token": access_token, "token_type": "bearer"}
