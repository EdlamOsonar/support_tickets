"""Caso de uso: Login de usuario."""
from app.domain.repositories.user_repository import UserRepository
from app.application.services.auth_service import AuthService
from app.interfaces.schemas.user_schemas import Token


class LoginUserUseCase:
    """Caso de uso para autenticar un usuario."""
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    def execute(self, email: str, password: str) -> Token:
        """
        Autentica un usuario y retorna un token.
        
        Raises:
            ValueError: Si las credenciales son inválidas
        """
        user = self.auth_service.authenticate_user(email, password)
        if not user:
            raise ValueError("Email o contraseña incorrectos")
        
        access_token = self.auth_service.create_access_token_for_user(user)
        return Token(access_token=access_token, token_type="bearer")

