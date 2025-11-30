"""Interfaz de repositorio de items (puerto)."""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.item import Item
from app.domain.entities.item_status import ItemStatus


class ItemRepository(ABC):
    """Puerto para operaciones de items."""
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[Item]:
        """Obtiene un item por ID."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """Obtiene todos los items con paginación."""
        pass
    
    @abstractmethod
    def create(self, item: Item) -> Item:
        """Crea un nuevo item."""
        pass
    
    @abstractmethod
    def update(self, item: Item) -> Item:
        """Actualiza un item existente."""
        pass
    
    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """Elimina un item."""
        pass
    
    @abstractmethod
    def get_status_by_name(self, status: str) -> Optional[ItemStatus]:
        """Obtiene un estado por nombre."""
        pass
    
    @abstractmethod
    def get_all_statuses(self) -> List[ItemStatus]:
        """Obtiene todos los estados."""
        pass
    
    @abstractmethod
    def get_status_by_id(self, status_id: int) -> Optional[ItemStatus]:
        """Obtiene un estado por ID."""
        pass

