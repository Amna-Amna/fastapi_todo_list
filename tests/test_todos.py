from fastapi.testclient import TestClient
from fastapi import status
from fastapi_todo_list.tests.utils import *
from fastapi_todo_list.routers.todos import get_db, db_dependency, user_dependency
from fastapi_todo_list.routers.auth import get_current_user
from fastapi_todo_list.models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_todos(test_todo):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == test_todo.id
    assert data[0]["title"] == test_todo.title
    assert data[0]["description"] == test_todo.description
    assert data[0]["priority"] == test_todo.priority
    assert data[0]["completed"] == test_todo.completed


def test_get_todo(test_todo):
    response = client.get(f"/todos/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_todo.id
    assert data["title"] == test_todo.title
    assert data["description"] == test_todo.description
    assert data["priority"] == test_todo.priority
    assert data["completed"] == test_todo.completed


def test_create_todo(test_todo):
    response = client.post("/todos/", json={"title": "New Test Todo", "description": "New Test Description", "priority": 1, "completed": False, "created_at": "2024-01-01T00:00:00", "updated_at": "2024-01-01T00:00:00"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "New Test Todo"
    assert data["description"] == "New Test Description"
    assert data["priority"] == 1
    assert data["completed"] == False


def test_update_todo(test_todo):
    response = client.put(f"/todos/{test_todo.id}", json={"title": "Updated Todo", "description": "Updated Description", "priority": 2, "completed": True, "created_at": "2024-01-01T00:00:00", "updated_at": "2024-01-01T00:00:00"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["priority"] == 2
    assert data["completed"] == True


def test_delete_todo(test_todo):
    response = client.delete(f"/todos/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Todo deleted successfully"


