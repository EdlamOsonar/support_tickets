"""Implementación de repositorio de usuarios."""
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.database.models.user_model import User as SQLAlchemyUser
from app.infrastructure.database.mappers import user_to_domain, user_to_db


class UserRepositoryImpl(UserRepository):
    """Implementación del repositorio de usuarios."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por email."""
        db_user = self.db.query(SQLAlchemyUser).filter(SQLAlchemyUser.email == email).first()
        if db_user is None:
            return None
        return user_to_domain(db_user)
    
    def create(self, user: User) -> User:
        """Crea un nuevo usuario."""
        db_user = user_to_db(user)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return user_to_domain(db_user)

