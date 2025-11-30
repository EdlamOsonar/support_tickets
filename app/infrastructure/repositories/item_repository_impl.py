"""Implementación de repositorio de items."""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.repositories.item_repository import ItemRepository
from app.domain.entities.item import Item
from app.domain.entities.item_status import ItemStatus
from app.infrastructure.database.models.item_model import Item as SQLAlchemyItem
from app.infrastructure.database.models.item_status_model import ItemStatus as SQLAlchemyItemStatus
from app.infrastructure.database.mappers import (
    item_to_domain,
    item_to_db,
    item_status_to_domain,
)


class ItemRepositoryImpl(ItemRepository):
    """Implementación del repositorio de items."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, item_id: int) -> Optional[Item]:
        """Obtiene un item por ID."""
        db_item = self.db.query(SQLAlchemyItem).filter(SQLAlchemyItem.id == item_id).first()
        if db_item is None:
            return None
        return item_to_domain(db_item)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """Obtiene todos los items con paginación."""
        db_items = self.db.query(SQLAlchemyItem).offset(skip).limit(limit).all()
        return [item_to_domain(db_item) for db_item in db_items]
    
    def create(self, item: Item) -> Item:
        """Crea un nuevo item."""
        db_item = item_to_db(item)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return item_to_domain(db_item)
    
    def update(self, item: Item) -> Item:
        """Actualiza un item existente."""
        db_item = self.db.query(SQLAlchemyItem).filter(SQLAlchemyItem.id == item.id).first()
        if db_item is None:
            raise ValueError(f"Item con id {item.id} no encontrado")
        
        # Actualizar campos
        db_item.name = item.name
        db_item.description = item.description
        db_item.ticket_url = item.ticket_url
        db_item.publication_url = item.publication_url
        db_item.reported_user = item.reported_user
        db_item.status_id = item.status_id
        
        self.db.commit()
        self.db.refresh(db_item)
        return item_to_domain(db_item)
    
    def delete(self, item_id: int) -> bool:
        """Elimina un item."""
        db_item = self.db.query(SQLAlchemyItem).filter(SQLAlchemyItem.id == item_id).first()
        if not db_item:
            return False
        self.db.delete(db_item)
        self.db.commit()
        return True
    
    def get_status_by_name(self, status: str) -> Optional[ItemStatus]:
        """Obtiene un estado por nombre."""
        db_status = self.db.query(SQLAlchemyItemStatus).filter(
            SQLAlchemyItemStatus.status == status
        ).first()
        if db_status is None:
            return None
        return item_status_to_domain(db_status)
    
    def get_all_statuses(self) -> List[ItemStatus]:
        """Obtiene todos los estados."""
        db_statuses = self.db.query(SQLAlchemyItemStatus).all()
        return [item_status_to_domain(db_status) for db_status in db_statuses]
    
    def get_status_by_id(self, status_id: int) -> Optional[ItemStatus]:
        """Obtiene un estado por ID."""
        db_status = self.db.query(SQLAlchemyItemStatus).filter(
            SQLAlchemyItemStatus.id == status_id
        ).first()
        if db_status is None:
            return None
        return item_status_to_domain(db_status)

