from sqlalchemy.orm import Session
from . import models, schemas


# ====== ItemStatus CRUD ======

def get_item_status_by_name(db: Session, status: str):
    return db.query(models.ItemStatus).filter(models.ItemStatus.status == status).first()


def get_all_item_statuses(db: Session):
    return db.query(models.ItemStatus).all()


# ====== Item CRUD ======

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    # Get the IN_PROGRESS status (default status)
    status = get_item_status_by_name(db, "IN_PROGRESS")
    
    db_item = models.Item(
        name=item.name,
        description=item.description,
        ticket_url=item.ticket_url,
        publication_url=item.publication_url,
        reported_user=item.reported_user,
        status_id=status.id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    db_item.name = item.name
    db_item.description = item.description
    db_item.ticket_url = item.ticket_url
    db_item.publication_url = item.publication_url
    db_item.reported_user = item.reported_user
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item_status(db: Session, item_id: int, status: str):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    status_obj = get_item_status_by_name(db, status)
    if not status_obj:
        return None
    
    db_item.status_id = status_obj.id
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True
