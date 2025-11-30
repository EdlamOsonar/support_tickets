"""Aplicación FastAPI principal."""
from fastapi import FastAPI

from app.interfaces.api.routes import auth, items

app = FastAPI(title="Ticketing System API", version="1.0.0")

# Incluir routers
app.include_router(auth.router)
app.include_router(items.router)


@app.get("/health", tags=["health"])
def health():
    """Health check endpoint (público)."""
    return {"status": "ok"}

