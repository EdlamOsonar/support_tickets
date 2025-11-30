"""Modelo SQLAlchemy de ItemStatus."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class ItemStatus(Base):
    """Modelo de estado de item."""
    __tablename__ = "items_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), nullable=False, unique=True, index=True)

    items = relationship("Item", back_populates="status_rel")

