from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


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


class ItemStatus(Base):
    __tablename__ = "items_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), nullable=False, unique=True, index=True)

    items = relationship("Item", back_populates="status_rel")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, index=True)
    description = Column(Text, nullable=True)
    ticket_url = Column(String(255), nullable=True)
    publication_url = Column(String(255), nullable=True)
    reported_user = Column(String(128), nullable=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status_id = Column(Integer, ForeignKey("items_status.id"), nullable=False, default=1)

    status_rel = relationship("ItemStatus", back_populates="items")
