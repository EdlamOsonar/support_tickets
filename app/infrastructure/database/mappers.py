"""Mappers entre entidades de dominio y modelos SQLAlchemy."""
from app.domain.entities.user import User as DomainUser
from app.domain.entities.item import Item as DomainItem
from app.domain.entities.item_status import ItemStatus as DomainItemStatus
from app.infrastructure.database.models.user_model import User as SQLAlchemyUser
from app.infrastructure.database.models.item_model import Item as SQLAlchemyItem
from app.infrastructure.database.models.item_status_model import ItemStatus as SQLAlchemyItemStatus


def user_to_domain(db_user: SQLAlchemyUser) -> DomainUser:
    """Convierte un modelo SQLAlchemy User a entidad de dominio."""
    return DomainUser(
        id=db_user.id,
        email=db_user.email,
        hashed_password=db_user.hashed_password,
        full_name=db_user.full_name,
        role=db_user.role,
        is_active=db_user.is_active,
        created_at=db_user.created_at
    )


def user_to_db(domain_user: DomainUser) -> SQLAlchemyUser:
    """Convierte una entidad de dominio User a modelo SQLAlchemy."""
    return SQLAlchemyUser(
        id=domain_user.id,
        email=domain_user.email,
        hashed_password=domain_user.hashed_password,
        full_name=domain_user.full_name,
        role=domain_user.role,
        is_active=domain_user.is_active,
        created_at=domain_user.created_at
    )


def item_to_domain(db_item: SQLAlchemyItem) -> DomainItem:
    """Convierte un modelo SQLAlchemy Item a entidad de dominio."""
    return DomainItem(
        id=db_item.id,
        name=db_item.name,
        description=db_item.description,
        ticket_url=db_item.ticket_url,
        publication_url=db_item.publication_url,
        reported_user=db_item.reported_user,
        creation_date=db_item.creation_date,
        status_id=db_item.status_id
    )


def item_to_db(domain_item: DomainItem) -> SQLAlchemyItem:
    """Convierte una entidad de dominio Item a modelo SQLAlchemy."""
    return SQLAlchemyItem(
        id=domain_item.id,
        name=domain_item.name,
        description=domain_item.description,
        ticket_url=domain_item.ticket_url,
        publication_url=domain_item.publication_url,
        reported_user=domain_item.reported_user,
        creation_date=domain_item.creation_date,
        status_id=domain_item.status_id
    )


def item_status_to_domain(db_status: SQLAlchemyItemStatus) -> DomainItemStatus:
    """Convierte un modelo SQLAlchemy ItemStatus a entidad de dominio."""
    return DomainItemStatus(
        id=db_status.id,
        status=db_status.status
    )


def item_status_to_db(domain_status: DomainItemStatus) -> SQLAlchemyItemStatus:
    """Convierte una entidad de dominio ItemStatus a modelo SQLAlchemy."""
    return SQLAlchemyItemStatus(
        id=domain_status.id,
        status=domain_status.status
    )

