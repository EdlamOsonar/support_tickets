"""Interfaz de repositorio de usuarios (puerto)."""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User


class UserRepository(ABC):
    """Puerto para operaciones de usuarios."""
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por email."""
        pass
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Crea un nuevo usuario."""
        pass

