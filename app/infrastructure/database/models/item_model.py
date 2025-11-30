"""Modelo SQLAlchemy de Item."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.database.base import Base


class Item(Base):
    """Modelo de item/ticket."""
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

