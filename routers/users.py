from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from pydantic import BaseModel, EmailStr
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import User, UserCreate, UserResponse
from ..database_conn import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: db_dependency, user: user_dependency):
    users = db.query(User).all()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return users

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(db: db_dependency, user_id: int, user: user_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(db: db_dependency, user_request: UserCreate):
    user = User(
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        hashed_password=bcrypt_context.hash(user_request.hashed_password),
        role=user_request.role,
        is_active=user_request.is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_user(db: db_dependency, user_id: int, user_request: UserCreate, user: user_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.username = user_request.username
    user.first_name = user_request.first_name
    user.last_name = user_request.last_name
    user.email = user_request.email
    user.hashed_password = bcrypt_context.hash(user_request.hashed_password)
    user.role = user_request.role
    user.is_active = user_request.is_active
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(db: db_dependency, user_id: int, user: user_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}