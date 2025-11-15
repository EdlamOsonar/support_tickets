from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

# Base.metadata.create_all(bind=engine)  # Commented out: Using Alembic for migrations

app = FastAPI(title="Ticeting System API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/items/", response_model=schemas.Item, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip, limit)


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.patch("/items/{item_id}/status", response_model=schemas.Item)
def update_item_status(item_id: int, status: str, db: Session = Depends(get_db)):
    if status not in ["IN_PROGRESS", "RESOLVED"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'IN_PROGRESS' or 'RESOLVED'")
    
    db_item = crud.update_item_status(db, item_id, status)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_item(db, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return


@app.get("/statuses/", response_model=list[schemas.ItemStatus])
def get_statuses(db: Session = Depends(get_db)):
    return crud.get_all_item_statuses(db)


@app.get("/health")
def health():
    return {"status": "ok"}
