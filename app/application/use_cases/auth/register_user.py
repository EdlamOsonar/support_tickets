"""Caso de uso: Registrar usuario."""
from datetime import datetime
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.application.services.auth_service import AuthService
from app.interfaces.schemas.user_schemas import UserCreate


class RegisterUserUseCase:
    """Caso de uso para registrar un nuevo usuario."""
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    def execute(self, user_data: UserCreate) -> User:
        """
        Registra un nuevo usuario.
        
        Raises:
            ValueError: Si el email ya está registrado o la contraseña es inválida
        """
        # Verificar si el usuario ya existe
        if self.user_repository.get_by_email(user_data.email):
            raise ValueError("El email ya está registrado")
        
        # Crear nuevo usuario
        db_user = User(
            email=user_data.email,
            hashed_password=self.auth_service.hash_password(user_data.password),
            full_name=user_data.full_name,
            role="user",
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        return self.user_repository.create(db_user)

