"""
Módulo de autenticación JWT con OAuth2.
Proporciona funciones para crear/verificar tokens y dependencias de FastAPI para proteger endpoints.
"""
import os
from datetime import datetime, timedelta
from typing import Optional, List

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal

# Configuración - Usar variables de entorno en producción
SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura-cambiar-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Contexto de encriptación para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 - apunta al endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    """Dependencia para obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera hash bcrypt de la contraseña."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT con los datos proporcionados.
    
    Args:
        data: Diccionario con datos a incluir en el token (ej: {"sub": email})
        expires_delta: Tiempo de expiración opcional
    
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Busca un usuario por su email."""
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """
    Autentica un usuario por email y contraseña.
    
    Returns:
        Usuario si las credenciales son válidas, None en caso contrario
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
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
        current_user: models.User = Depends(get_current_active_user)
    ) -> models.User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción"
            )
        return current_user
    return role_checker

