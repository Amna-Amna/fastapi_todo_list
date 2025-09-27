from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database_conn import SessionLocal
from ..models import Todos
from .auth import get_current_user
from typing import Annotated
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/todos", tags=["todos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int
    completed: bool
    created_at: datetime
    updated_at: datetime


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
def get_todos(db: db_dependency, user: user_dependency):
    todos = db.query(Todos).filter(Todos.owner_id == user["user_id"]).all()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if todos is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todos not found")
    return todos


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo(db: db_dependency, user: user_dependency, todo_id: int):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, user: user_dependency, todo_request: TodoRequest):
    todo = Todos(
        title=todo_request.title,
        description=todo_request.description,
        priority=todo_request.priority,
        owner_id=user["user_id"],
        created_at=todo_request.created_at,
        updated_at=todo_request.updated_at
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
def update_todo(db: db_dependency, user: user_dependency, todo_id: int, todo_request: TodoRequest):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.completed = todo_request.completed
    todo.updated_at = todo_request.updated_at
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(db: db_dependency, user: user_dependency, todo_id: int):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {
        "message": "Todo deleted successfully"
    }