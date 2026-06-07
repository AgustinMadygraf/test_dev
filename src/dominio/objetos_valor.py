# Path: src/dominio/objetos_valor.py

from dataclasses import dataclass
import re
from src.dominio.excepciones import ErrorValorInvalido

@dataclass(frozen=True)
class CorreoElectronico:
    direccion: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.direccion):
            raise ErrorValorInvalido(f"Correo electrónico inválido: {self.direccion}")

    def __str__(self):
        return self.direccion

@dataclass(frozen=True)
class NumeroExpediente:
    valor: str

    def __post_init__(self):
        valor_a_validar = self.valor.valor if isinstance(self.valor, NumeroExpediente) else self.valor
        if not re.match(r"^[a-zA-Z0-9\-]+$", valor_a_validar):
            raise ErrorValorInvalido(f"Formato de número de expediente inválido: {valor_a_validar}")

    def __str__(self):
        return str(self.valor)
