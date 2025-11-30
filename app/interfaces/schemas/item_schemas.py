"""Schemas de items/tickets."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemStatusBase(BaseModel):
    status: str


class ItemStatus(ItemStatusBase):
    id: int

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    ticket_url: Optional[str] = None
    publication_url: Optional[str] = None
    reported_user: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    creation_date: datetime
    status_id: int
    status_rel: ItemStatus

    class Config:
        from_attributes = True

