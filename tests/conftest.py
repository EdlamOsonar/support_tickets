import os
import sys
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import Base, get_db
from app.main import app


@pytest.fixture(scope='session')
def engine():
    # Use in-memory SQLite for tests
    engine = create_engine('sqlite:///:memory:', connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture()
def db_session(engine):
    SessionTesting = sessionmaker(bind=engine)
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session, monkeypatch):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    monkeypatch.setattr('app.main.get_db', override_get_db)
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c
