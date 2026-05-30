"""
Path: src/domain/entities/user.py
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    hashed_password: str
    id: Optional[int] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
