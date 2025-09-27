from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_todo_list.database_conn import Base
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from fastapi_todo_list.main import app
import pytest
from fastapi_todo_list.models import User, Todos
from datetime import datetime
from sqlalchemy import text


SQLITE_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"user_id": 1, "username": "test"}


@pytest.fixture()
def test_user():
    db = TestingSessionLocal()
    db.execute(text("DELETE FROM users"))
    db.commit()
    
    user = User(
        username="test",
        role="user",
        first_name="test",
        last_name="test",
        email="test@test.com",
        hashed_password="test",
        is_active=True,
        phone_number=None
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    
    db.execute(text("DELETE FROM users"))
    db.commit()
    db.close()

@pytest.fixture()
def test_todo():
    db = TestingSessionLocal()
    db.execute(text("DELETE FROM todos"))
    db.commit()
    
    todo = Todos(
        title="Test Todo",
        description="Test Description",
        priority=1,
        completed=False,
        owner_id=1)

    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    
    db.execute(text("DELETE FROM todos"))
    db.commit()
    db.close()