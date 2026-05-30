"""
Path: src/entities/user.py
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    email: str = ""
    hashed_password: str = ""
    full_name: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
