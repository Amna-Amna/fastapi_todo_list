import pytest
from fastapi_todo_list.tests.utils import *
from fastapi_todo_list.models import User
from starlette import status
from fastapi_todo_list.routers.users import get_db, db_dependency, user_dependency
from fastapi_todo_list.routers.auth import get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_users(test_user):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data) == 1
    user_data = data[0]
    
    user_data.pop("created_at")
    user_data.pop("updated_at")
    user_data.pop("hashed_password")
    
    expected = {
        "id": test_user.id,
        "username": test_user.username,
        "first_name": test_user.first_name,
        "last_name": test_user.last_name,
        "email": test_user.email,
        "role": test_user.role,
        "is_active": test_user.is_active,
        "phone_number": test_user.phone_number,
    }
    
    assert user_data == expected


def test_create_user(test_user):
    user_request = {
        "username": "newuser",
        "first_name": "test",
        "last_name": "test",
        "email": "newuser@test.com",
        "role": "user",
        "hashed_password": "password123",
        "is_active": True,
        "phone_number": None
    }

    response = client.post("/users/", json=user_request)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    created = db.query(User).filter(User.id == response.json()["id"]).first()
    assert created is not None
    assert created.username == user_request.get("username")
    assert created.first_name == user_request.get("first_name")
    assert created.last_name == user_request.get("last_name")
    assert created.email == user_request.get("email")
    assert created.role == user_request.get("role")
    assert created.is_active == user_request.get("is_active")
    assert created.phone_number == user_request.get("phone_number")
    db.close()


def test_get_user(test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username
    assert data["first_name"] == test_user.first_name
    assert data["last_name"] == test_user.last_name
    assert data["email"] == test_user.email
    assert data["role"] == test_user.role
    assert data["is_active"] == test_user.is_active
    assert data["phone_number"] == test_user.phone_number

def test_update_user(test_user):
    user_request = {
        "username": "newuser",
        "first_name": "test",
        "last_name": "test",
        "email": "newuser@test.com",
        "role": "user",
        "hashed_password": "password123",
        "is_active": True,
        "phone_number": None
    }
    response = client.put(f"/users/{test_user.id}", json=user_request)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == user_request.get("username")
    assert data["first_name"] == user_request.get("first_name")
    assert data["last_name"] == user_request.get("last_name")
    assert data["email"] == user_request.get("email")
    assert data["role"] == user_request.get("role")
    assert data["is_active"] == user_request.get("is_active")
    assert data["phone_number"] == user_request.get("phone_number")

def test_delete_user(test_user):
    response = client.delete(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "User deleted successfully"
    
    db = TestingSessionLocal()
    user = db.query(User).filter(User.id == test_user.id).first()
    assert user is None
    db.close()


def test_get_user_not_found(test_user):
    response = client.get(f"/users/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User not found"
    
def test_update_user_not_found(test_user):
    user_request = {
        "username": "newuser",
        "first_name": "test",
        "last_name": "test",
        "email": "newuser@test.com",
        "role": "user",
        "hashed_password": "password123",
        "is_active": True,
        "phone_number": None
    }
    response = client.put(f"/users/999999", json=user_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User not found"


def test_delete_user_not_found(test_user):
    response = client.delete(f"/users/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User not found"
    
