# Path: src/domain/value_objects.py

from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Email:
    address: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.address):
            from src.domain.exceptions import InvalidValueError
            raise InvalidValueError(f"Email inválido: {self.address}")

    def __str__(self):
        return self.address

@dataclass(frozen=True)
class NumeroExpediente:
    valor: str

    def __post_init__(self):
        # Permitir números, letras y guiones
        valor = self.valor.valor if isinstance(self.valor, NumeroExpediente) else self.valor
        if not re.match(r"^[a-zA-Z0-9\-]+$", valor):
            from src.domain.exceptions import InvalidValueError
            raise InvalidValueError(f"Formato de número de expediente inválido: {valor}")

    def __str__(self):
        return str(self.valor)
