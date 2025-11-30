"""Caso de uso: Actualizar item."""
from typing import Optional
from app.domain.repositories.item_repository import ItemRepository
from app.domain.entities.item import Item
from app.interfaces.schemas.item_schemas import ItemCreate


class UpdateItemUseCase:
    """Caso de uso para actualizar un item."""
    
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
    
    def execute(self, item_id: int, item_data: ItemCreate) -> Optional[Item]:
        """Actualiza un item existente."""
        db_item = self.item_repository.get_by_id(item_id)
        if not db_item:
            return None
        
        db_item.name = item_data.name
        db_item.description = item_data.description
        db_item.ticket_url = item_data.ticket_url
        db_item.publication_url = item_data.publication_url
        db_item.reported_user = item_data.reported_user
        
        return self.item_repository.update(db_item)

