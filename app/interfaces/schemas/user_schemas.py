"""Schemas de usuario."""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Valida la contraseña:
        - Mínimo 8 caracteres
        - Máximo 72 bytes (límite de bcrypt)
        - Acepta letras, números y caracteres especiales
        """
        # Eliminar espacios en blanco al inicio y final
        v = v.strip()
        
        # Validar longitud mínima
        if len(v) < 8:
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres. "
                "Ejemplo de formato válido: (Aion__2025)"
            )
        
        # Validar longitud máxima en bytes (límite de bcrypt)
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError(
                "La contraseña no puede tener más de 72 bytes. "
                "Por favor, usa una contraseña más corta."
            )
        
        # La contraseña puede contener cualquier carácter (letras, números, símbolos)
        # No restringimos caracteres especiales como paréntesis, guiones bajos, etc.
        return v


class User(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

