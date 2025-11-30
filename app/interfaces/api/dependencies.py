"""Dependencias de FastAPI para autenticación y autorización."""
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.infrastructure.database.session import get_db
from app.domain.entities.user import User
from app.infrastructure.security.jwt_handler import decode_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

# Esquema OAuth2 - apunta al endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependencia para obtener el repositorio de usuarios."""
    return UserRepositoryImpl(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    """
    Dependencia que extrae y valida el usuario del token JWT.
    
    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependencia que verifica que el usuario esté activo.
    
    Raises:
        HTTPException 400: Si el usuario está inactivo
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user


def require_role(allowed_roles: List[str]):
    """
    Factory de dependencias para verificar roles de usuario.
    
    Args:
        allowed_roles: Lista de roles permitidos (ej: ["admin", "agent"])
    
    Returns:
        Dependencia de FastAPI que verifica el rol
    
    Example:
        @app.delete("/items/{id}")
        def delete_item(current_user = Depends(require_role(["admin"]))):
            ...
    """
    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción"
            )
        return current_user
    return role_checker

