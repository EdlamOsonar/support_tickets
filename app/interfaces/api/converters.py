"""Convertidores entre entidades de dominio y schemas Pydantic."""
from app.domain.entities.user import User as DomainUser
from app.domain.entities.item import Item as DomainItem
from app.domain.entities.item_status import ItemStatus as DomainItemStatus
from app.interfaces.schemas.user_schemas import User as UserSchema
from app.interfaces.schemas.item_schemas import Item as ItemSchema, ItemStatus as ItemStatusSchema


def domain_user_to_schema(domain_user: DomainUser) -> UserSchema:
    """Convierte una entidad de dominio User a schema Pydantic."""
    return UserSchema(
        id=domain_user.id,
        email=domain_user.email,
        full_name=domain_user.full_name,
        role=domain_user.role,
        is_active=domain_user.is_active,
        created_at=domain_user.created_at
    )


def domain_item_to_schema(domain_item: DomainItem, status: DomainItemStatus) -> ItemSchema:
    """Convierte una entidad de dominio Item a schema Pydantic."""
    return ItemSchema(
        id=domain_item.id,
        name=domain_item.name,
        description=domain_item.description,
        ticket_url=domain_item.ticket_url,
        publication_url=domain_item.publication_url,
        reported_user=domain_item.reported_user,
        creation_date=domain_item.creation_date,
        status_id=domain_item.status_id,
        status_rel=ItemStatusSchema(
            id=status.id,
            status=status.status
        )
    )


def domain_item_status_to_schema(domain_status: DomainItemStatus) -> ItemStatusSchema:
    """Convierte una entidad de dominio ItemStatus a schema Pydantic."""
    return ItemStatusSchema(
        id=domain_status.id,
        status=domain_status.status
    )

