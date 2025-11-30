"""Entidad de dominio: Usuario."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Entidad de dominio de usuario."""
    id: Optional[int] = None
    email: str = ""
    hashed_password: str = ""
    full_name: Optional[str] = None
    role: str = "user"
    is_active: bool = True
    created_at: Optional[datetime] = None

