"""Rutas de autenticación."""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.domain.entities.user import User
from app.interfaces.api.converters import domain_user_to_schema
from app.domain.repositories.user_repository import UserRepository
from app.application.services.auth_service import AuthService
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.interfaces.schemas import User as UserSchema, UserCreate, Token
from app.interfaces.api.dependencies import (
    get_current_active_user,
    get_user_repository,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    """Dependencia para obtener el servicio de autenticación."""
    return AuthService(user_repo)


@router.post("/register", response_model=UserSchema, status_code=201)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Registra un nuevo usuario.
    
    - **email**: Email único del usuario
    - **password**: Contraseña (se almacenará hasheada, máximo 72 bytes)
    - **full_name**: Nombre completo (opcional)
    """
    try:
        use_case = RegisterUserUseCase(user_repo, auth_service)
        domain_user = use_case.execute(user)
        return domain_user_to_schema(domain_user)
    except ValueError as e:
        # Capturar errores de validación de contraseña o email duplicado
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al registrar usuario: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Inicia sesión y obtiene un token JWT.
    
    Usa OAuth2 password flow:
    - **username**: Email del usuario
    - **password**: Contraseña
    
    Retorna un access_token para usar en el header Authorization.
    """
    try:
        use_case = LoginUserUseCase(user_repo, auth_service)
        return use_case.execute(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserSchema)
def get_me(current_user: User = Depends(get_current_active_user)):
    """Obtiene la información del usuario autenticado."""
    return domain_user_to_schema(current_user)

