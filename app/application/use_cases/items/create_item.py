"""Caso de uso: Crear item."""
from app.domain.repositories.item_repository import ItemRepository
from app.domain.entities.item import Item
from app.interfaces.schemas.item_schemas import ItemCreate


class CreateItemUseCase:
    """Caso de uso para crear un nuevo item."""
    
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository
    
    def execute(self, item_data: ItemCreate) -> Item:
        """Crea un nuevo item."""
        # Obtener el estado IN_PROGRESS (estado por defecto)
        status = self.item_repository.get_status_by_name("IN_PROGRESS")
        if not status:
            raise ValueError("Estado IN_PROGRESS no encontrado")
        
        db_item = Item(
            name=item_data.name,
            description=item_data.description,
            ticket_url=item_data.ticket_url,
            publication_url=item_data.publication_url,
            reported_user=item_data.reported_user,
            status_id=status.id
        )
        
        return self.item_repository.create(db_item)

