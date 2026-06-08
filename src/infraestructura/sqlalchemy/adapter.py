from typing import List, Optional, Any, cast
from src.dominio.entidades.expediente import Expediente
from src.dominio.entidades.usuario import Usuario
from src.dominio.servicios.repositorios import IRepositorioExpediente, IRepositorioUsuario
from src.infraestructura.sqlalchemy.models import ExpedienteORM, UsuarioORM
from sqlalchemy.orm import Session

class SQLAlchemyDatabaseAdapter(IRepositorioExpediente):
    def __init__(self, session: Session):
        self.session = session

    def guardar(self, expediente: Expediente) -> Expediente:
        if expediente.id:
            obj = self.session.get(ExpedienteORM, expediente.id)
            if obj:
                orm_obj = cast(Any, obj)
                orm_obj.numero = str(expediente.numero)
                orm_obj.extracto = expediente.extracto
                orm_obj.descripcion = expediente.descripcion
                orm_obj.estado = expediente.estado
                orm_obj.id_propietario = expediente.id_propietario
                self.session.flush()
                return self._to_entity(obj)
        
        new_obj = ExpedienteORM(
            numero=str(expediente.numero),
            extracto=expediente.extracto,
            id_propietario=expediente.id_propietario,
            descripcion=expediente.descripcion,
            estado=expediente.estado
        )
        self.session.add(new_obj)
        self.session.flush()
        self.session.refresh(new_obj)
        return self._to_entity(new_obj)

    def buscar_por_numero(self, numero: str) -> Optional[Expediente]:
        obj = self.session.query(ExpedienteORM).filter_by(numero=numero).first()
        return self._to_entity(obj) if obj else None

    def buscar_por_id(self, expediente_id: int) -> Optional[Expediente]:
        obj = self.session.get(ExpedienteORM, expediente_id)
        return self._to_entity(obj) if obj else None

    def buscar_todos(self, id_propietario: Optional[int] = None) -> List[Expediente]:
        query = self.session.query(ExpedienteORM)
        if id_propietario:
            query = query.filter_by(id_propietario=id_propietario)
        objs = query.all()
        return [self._to_entity(obj) for obj in objs]

    def _to_entity(self, orm: ExpedienteORM) -> Expediente:
        return Expediente(
            id=cast(Any, orm.id),
            numero=cast(Any, orm.numero),
            extracto=cast(Any, orm.extracto),
            id_propietario=cast(Any, orm.id_propietario),
            descripcion=cast(Any, orm.descripcion),
            estado=cast(Any, orm.estado),
            fecha_creacion=cast(Any, orm.fecha_creacion),
            ultima_modificacion=cast(Any, orm.ultima_modificacion)
        )

class SQLAlchemyUsuarioAdapter(IRepositorioUsuario):
    def __init__(self, session: Session):
        self.session = session

    def guardar(self, usuario: Usuario) -> Usuario:
        if usuario.id:
            obj = self.session.get(UsuarioORM, usuario.id)
            if obj:
                orm_obj = cast(Any, obj)
                orm_obj.correo = str(usuario.correo)
                orm_obj.contrasena_hash = usuario.contrasena_hash
                orm_obj.nombre_completo = usuario.nombre_completo
                orm_obj.es_activo = usuario.es_activo
                orm_obj.es_administrador = usuario.es_administrador
                self.session.flush()
                return self._to_entity(obj)
        
        new_obj = UsuarioORM(
            correo=str(usuario.correo),
            contrasena_hash=usuario.contrasena_hash,
            nombre_completo=usuario.nombre_completo,
            es_activo=usuario.es_activo,
            es_administrador=usuario.es_administrador
        )
        self.session.add(new_obj)
        self.session.flush()
        self.session.refresh(new_obj)
        return self._to_entity(new_obj)

    def buscar_por_correo(self, correo: str) -> Optional[Usuario]:
        obj = self.session.query(UsuarioORM).filter_by(correo=correo).first()
        return self._to_entity(obj) if obj else None

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        obj = self.session.get(UsuarioORM, usuario_id)
        return self._to_entity(obj) if obj else None

    def _to_entity(self, orm: UsuarioORM) -> Usuario:
        return Usuario(
            id=cast(Any, orm.id),
            correo=cast(Any, orm.correo),
            contrasena_hash=cast(Any, orm.contrasena_hash),
            nombre_completo=cast(Any, orm.nombre_completo),
            es_activo=cast(Any, orm.es_activo),
            es_administrador=cast(Any, orm.es_administrador)
        )
