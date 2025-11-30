"""Caso de uso: Eliminar item."""
from app.domain.repositories.item_repository import ItemRepository


class DeleteItemUseCase:
    """Caso de uso para eliminar un item."""
    
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
    
    def execute(self, item_id: int) -> bool:
        """Elimina un item."""
        return self.item_repository.delete(item_id)

