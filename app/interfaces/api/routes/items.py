"""Rutas de items/tickets."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.domain.entities.user import User
from app.domain.repositories.item_repository import ItemRepository
from app.infrastructure.repositories.item_repository_impl import ItemRepositoryImpl
from app.application.use_cases.items.create_item import CreateItemUseCase
from app.application.use_cases.items.get_item import GetItemUseCase
from app.application.use_cases.items.list_items import ListItemsUseCase
from app.application.use_cases.items.update_item import UpdateItemUseCase
from app.application.use_cases.items.update_item_status import UpdateItemStatusUseCase
from app.application.use_cases.items.delete_item import DeleteItemUseCase
from app.application.use_cases.items.get_statuses import GetStatusesUseCase
from app.interfaces.schemas import Item, ItemCreate, ItemStatus
from app.interfaces.api.dependencies import get_current_active_user, require_role
from app.interfaces.api.converters import domain_item_to_schema, domain_item_status_to_schema

router = APIRouter(prefix="/items", tags=["items"])


def get_item_repository(db: Session = Depends(get_db)) -> ItemRepository:
    """Dependencia para obtener el repositorio de items."""
    return ItemRepositoryImpl(db)


@router.post("/", response_model=Item, status_code=201)
def create_item(
    item: ItemCreate,
    item_repo: ItemRepository = Depends(get_item_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crea un nuevo ticket de soporte.
    
    **Requiere autenticación.**
    """
    use_case = CreateItemUseCase(item_repo)
    domain_item = use_case.execute(item)
    status = item_repo.get_status_by_id(domain_item.status_id)
    if not status:
        raise HTTPException(status_code=500, detail="Estado no encontrado")
    return domain_item_to_schema(domain_item, status)


@router.get("/", response_model=list[Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    item_repo: ItemRepository = Depends(get_item_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todos los tickets con paginación.
    
    **Requiere autenticación.**
    """
    use_case = ListItemsUseCase(item_repo)
    domain_items = use_case.execute(skip, limit)
    result = []
    for domain_item in domain_items:
        status = item_repo.get_status_by_id(domain_item.status_id)
        if status:
            result.append(domain_item_to_schema(domain_item, status))
    return result


@router.get("/{item_id}", response_model=Item)
def read_item(
    item_id: int,
    item_repo: ItemRepository = Depends(get_item_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene un ticket específico por ID.
    
    **Requiere autenticación.**
    """
    use_case = GetItemUseCase(item_repo)
    domain_item = use_case.execute(item_id)
    if domain_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    status = item_repo.get_status_by_id(domain_item.status_id)
    if not status:
        raise HTTPException(status_code=500, detail="Estado no encontrado")
    return domain_item_to_schema(domain_item, status)


@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item: ItemCreate,
    item_repo: ItemRepository = Depends(get_item_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualiza un ticket existente.
    
    **Requiere autenticación.**
    """
    use_case = UpdateItemUseCase(item_repo)
    domain_item = use_case.execute(item_id, item)
    if domain_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    status = item_repo.get_status_by_id(domain_item.status_id)
    if not status:
        raise HTTPException(status_code=500, detail="Estado no encontrado")
    return domain_item_to_schema(domain_item, status)


@router.patch("/{item_id}/status", response_model=Item)
def update_item_status(
    item_id: int,
    status: str,
    item_repo: ItemRepository = Depends(get_item_repository),
    current_user: User = Depends(require_role(["admin", "agent"]))
):
    """
    Cambia el estado de un ticket.
    
    **Requiere rol: admin o agent.**
    
    Estados válidos: IN_PROGRESS, RESOLVED
    """
    if status not in ["IN_PROGRESS", "RESOLVED"]:
        raise HTTPException(
            status_code=400,
            detail="Estado inválido. Debe ser 'IN_PROGRESS' o 'RESOLVED'"
        )
    
    use_case = UpdateItemStatusUseCase(item_repo)
    domain_item = use_case.execute(item_id, status)
    if domain_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_status = item_repo.get_status_by_id(domain_item.status_id)
    if not item_status:
        raise HTTPException(status_code=500, detail="Estado no encontrado")
    return domain_item_to_schema(domain_item, item_status)


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    item_repo: ItemRepository = Depends(get_item_repository),
    current_user: User = Depends(require_role(["admin"]))
):
    """
    Elimina un ticket.
    
    **Requiere rol: admin.**
    """
    use_case = DeleteItemUseCase(item_repo)
    ok = use_case.execute(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return


@router.get("/statuses/", response_model=list[ItemStatus], tags=["statuses"])
def get_statuses(
    item_repo: ItemRepository = Depends(get_item_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todos los estados disponibles para tickets.
    
    **Requiere autenticación.**
    """
    use_case = GetStatusesUseCase(item_repo)
    domain_statuses = use_case.execute()
    return [domain_item_status_to_schema(status) for status in domain_statuses]

