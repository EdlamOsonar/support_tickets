"""Servicio de autenticación."""
from typing import Optional
from datetime import timedelta
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.security.password_handler import verify_password, get_password_hash
from app.infrastructure.security.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:
    """Servicio para operaciones de autenticación."""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su email."""
        return self.user_repository.get_by_email(email)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica un usuario por email y contraseña.
        
        Returns:
            Usuario si las credenciales son válidas, None en caso contrario
        """
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_access_token_for_user(self, user: User) -> str:
        """Crea un token de acceso para un usuario."""
        return create_access_token(
            data={"sub": user.email, "role": user.role},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    
    def hash_password(self, password: str) -> str:
        """Genera hash de contraseña."""
        return get_password_hash(password)

