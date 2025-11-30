"""Entidad de dominio: Item/Ticket."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Item:
    """Entidad de dominio de item/ticket."""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    ticket_url: Optional[str] = None
    publication_url: Optional[str] = None
    reported_user: Optional[str] = None
    creation_date: Optional[datetime] = None
    status_id: int = 1

