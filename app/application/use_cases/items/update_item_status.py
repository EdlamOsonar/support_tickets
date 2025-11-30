"""Caso de uso: Actualizar estado de item."""
from typing import Optional
from app.domain.repositories.item_repository import ItemRepository
from app.domain.entities.item import Item


class UpdateItemStatusUseCase:
    """Caso de uso para actualizar el estado de un item."""
    
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
    
    def execute(self, item_id: int, status: str) -> Optional[Item]:
        """Actualiza el estado de un item."""
        db_item = self.item_repository.get_by_id(item_id)
        if not db_item:
            return None
        
        status_obj = self.item_repository.get_status_by_name(status)
        if not status_obj:
            return None
        
        db_item.status_id = status_obj.id
        return self.item_repository.update(db_item)

