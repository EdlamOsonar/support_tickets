"""Modelo SQLAlchemy de Usuario."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.infrastructure.database.base import Base


class User(Base):
    """Modelo de usuario para autenticación y autorización."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(128), nullable=True)
    role = Column(String(20), nullable=False, default="user")  # admin, agent, user
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

