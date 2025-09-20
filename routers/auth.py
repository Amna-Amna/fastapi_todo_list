from ..database_conn import SessionLocal
from ..models import User
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from ..settings import base
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from jose import JWTError, jwt


router = APIRouter(prefix="/auth", tags=["auth"])

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(username: str, password:str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta | None = None):
    payload = {
        "sub": username,
        "id": user_id,
        "role": role,
    }
    # use configured expiry if not provided
    if expires_delta is None:
        expires_delta = timedelta(minutes=base.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(payload, base.SECRET_KEY, algorithm=base.ALGORITHM)

@router.post("/token", response_model=Token)
def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(user.username, user.id, user.role)
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, base.SECRET_KEY, algorithms=[base.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        return {
            "username": username,
            "user_id": user_id,
            "user_role": user_role
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")