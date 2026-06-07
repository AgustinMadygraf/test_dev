from dataclasses import dataclass
from typing import Optional
from src.domain.value_objects import Email

@dataclass
class User:
    email: Email
    hashed_password: str
    id: Optional[int] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False

    def __post_init__(self):
        if isinstance(self.email, str):
            self.email = Email(self.email)
