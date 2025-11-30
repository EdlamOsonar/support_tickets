"""Caso de uso: Obtener item."""
from typing import Optional
from app.domain.repositories.item_repository import ItemRepository
from app.domain.entities.item import Item


class GetItemUseCase:
    """Caso de uso para obtener un item por ID."""
    
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
    
    def execute(self, item_id: int) -> Optional[Item]:
        """Obtiene un item por ID."""
        return self.item_repository.get_by_id(item_id)

