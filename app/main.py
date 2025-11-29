from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .auth import (
    get_db,
    get_current_active_user,
    require_role,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Base.metadata.create_all(bind=engine)  # Commented out: Using Alembic for migrations

app = FastAPI(title="Ticketing System API", version="1.0.0")


# ========== AUTH ENDPOINTS ==========

@app.post("/auth/register", response_model=schemas.User, status_code=201, tags=["auth"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.
    
    - **email**: Email único del usuario
    - **password**: Contraseña (se almacenará hasheada)
    - **full_name**: Nombre completo (opcional)
    """
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    db_user = models.User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        role="user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/auth/login", response_model=schemas.Token, tags=["auth"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Inicia sesión y obtiene un token JWT.
    
    Usa OAuth2 password flow:
    - **username**: Email del usuario
    - **password**: Contraseña
    
    Retorna un access_token para usar en el header Authorization.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=schemas.User, tags=["auth"])
def get_me(current_user: models.User = Depends(get_current_active_user)):
    """Obtiene la información del usuario autenticado."""
    return current_user


# ========== ITEMS/TICKETS ENDPOINTS (PROTECTED) ==========

@app.post("/items/", response_model=schemas.Item, status_code=201, tags=["items"])
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Crea un nuevo ticket de soporte.
    
    **Requiere autenticación.**
    """
    return crud.create_item(db, item)


@app.get("/items/", response_model=list[schemas.Item], tags=["items"])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Lista todos los tickets con paginación.
    
    **Requiere autenticación.**
    """
    return crud.get_items(db, skip, limit)


@app.get("/items/{item_id}", response_model=schemas.Item, tags=["items"])
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Obtiene un ticket específico por ID.
    
    **Requiere autenticación.**
    """
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=schemas.Item, tags=["items"])
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Actualiza un ticket existente.
    
    **Requiere autenticación.**
    """
    db_item = crud.update_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.patch("/items/{item_id}/status", response_model=schemas.Item, tags=["items"])
def update_item_status(
    item_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin", "agent"]))
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
    
    db_item = crud.update_item_status(db, item_id, status)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.delete("/items/{item_id}", status_code=204, tags=["items"])
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    """
    Elimina un ticket.
    
    **Requiere rol: admin.**
    """
    ok = crud.delete_item(db, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return


@app.get("/statuses/", response_model=list[schemas.ItemStatus], tags=["statuses"])
def get_statuses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Lista todos los estados disponibles para tickets.
    
    **Requiere autenticación.**
    """
    return crud.get_all_item_statuses(db)


# ========== HEALTH CHECK ==========

@app.get("/health", tags=["health"])
def health():
    """Health check endpoint (público)."""
    return {"status": "ok"}
