"""Caso de uso: Listar items."""
from typing import List
from app.domain.repositories.item_repository import ItemRepository
from app.domain.entities.item import Item


class ListItemsUseCase:
    """Caso de uso para listar items."""
    
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
    
    def execute(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """Lista items con paginación."""
        return self.item_repository.get_all(skip, limit)

