from dataclasses import dataclass
from typing import Optional
from src.domain.objetos_valor import CorreoElectronico

@dataclass
class Usuario:
    correo: CorreoElectronico
    contrasena_hash: str
    id: Optional[int] = None
    nombre_completo: Optional[str] = None
    es_activo: bool = True
    es_administrador: bool = False

    def __post_init__(self):
        if isinstance(self.correo, str):
            self.correo = CorreoElectronico(self.correo)
