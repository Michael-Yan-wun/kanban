from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, deps
from ..database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=schemas.Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=login_data.username)
    if not db_user or not crud.verify_password(login_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    token = crud.create_auth_token(db, user_id=db_user.id)
    return {
        "access_token": token,
        "token_type": "token", 
        "user": db_user
    }

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user = Depends(deps.get_current_user)):
    return current_user
