from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ========== Auth Schemas ==========

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ========== Item Schemas ==========

class ItemStatusBase(BaseModel):
    status: str


class ItemStatus(ItemStatusBase):
    id: int

    class Config:
        orm_mode = True


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
        orm_mode = True
