from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from .database import get_db
from . import crud, models

# 定義 Header 格式: Authorization: Token <key>
# 不過 APIKeyHeader 只會取值，我們需要自己解析 "Token " 前綴
header_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def get_current_user(
    token_header: str = Depends(header_scheme),
    db: Session = Depends(get_db)
):
    if not token_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization Header",
        )
    
    # 支援 "Token <xxx>" 或直接 "<xxx>"
    token = token_header
    if token.startswith("Token "):
        token = token.split(" ")[1]
        
    user = crud.get_user_by_token(db, token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )
    return user

def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
