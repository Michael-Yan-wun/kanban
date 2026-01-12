from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import crud, schemas, models, deps
from ..database import get_db

router = APIRouter()

# 輔助函數：檢查是否為 Admin
def check_admin(current_user: models.User):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires admin privileges"
        )

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    # 限制只有管理員可以看所有用戶？或者開放給所有人看成員列表？
    # 這裡假設只有 Admin 能管理。如果是一般成員看 Member 列表，可以另開權限。
    # 為了方便，先允許所有登入用戶讀取列表 (用於看板成員顯示)，但在 User Management 介面通常是 Admin。
    # 既然是 "User Management CRUD"，我們稍微寬鬆一點，讓大家能看到成員，但只有 Admin 能刪改。
    return crud.get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    check_admin(current_user)
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate, # 我們需要定義這個 schema
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    check_admin(current_user)
    updated_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    check_admin(current_user)
    # 不允許刪除自己
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.post("/{user_id}/reset_password")
def reset_password(
    user_id: int,
    password_data: schemas.UserPasswordReset, # 需要定義
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    check_admin(current_user)
    success = crud.reset_password(db, user_id=user_id, new_password=password_data.password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password reset successfully"}
