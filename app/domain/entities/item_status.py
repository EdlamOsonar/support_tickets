"""Entidad de dominio: Estado de Item."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemStatus:
    """Entidad de dominio de estado de item."""
    id: Optional[int] = None
    status: str = ""

