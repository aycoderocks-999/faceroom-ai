import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("JWT_SECRET", "test-secret-key-for-pytest-only")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "password123"},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
