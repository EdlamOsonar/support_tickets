"""Caso de uso: Obtener estados."""
from typing import List
from app.domain.repositories.item_repository import ItemRepository
from app.domain.entities.item_status import ItemStatus


class GetStatusesUseCase:
    """Caso de uso para obtener todos los estados."""
    
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
    
    def execute(self) -> List[ItemStatus]:
        """Obtiene todos los estados disponibles."""
        return self.item_repository.get_all_statuses()

