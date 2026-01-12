from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import crud, schemas, deps
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ColumnResponse)
def create_column(
    column: schemas.ColumnCreate,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    # 檢查權限：使用者是否為該 board 的擁有者
    board = crud.get_board_by_id(db, board_id=column.board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return crud.create_column(db=db, column=column)

@router.get("/", response_model=List[schemas.ColumnResponse])
def read_columns(
    board_id: int,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    # 檢查權限同樣需要
    return crud.get_columns_by_board(db, board_id=board_id)

@router.put("/{column_id}", response_model=schemas.ColumnResponse)
def update_column(
    column_id: int,
    column_update: schemas.ColumnUpdate,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    db_column = crud.get_column(db, column_id=column_id)
    if not db_column:
        raise HTTPException(status_code=404, detail="Column not found")
        
    # Check permissions (via board ownership)
    board = crud.get_board_by_id(db, board_id=db_column.board_id)
    if not board or board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    return crud.update_column(db, column_id=column_id, column_update=column_update)

@router.delete("/{column_id}")
def delete_column(
    column_id: int,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    db_column = crud.get_column(db, column_id=column_id)
    if not db_column:
        raise HTTPException(status_code=404, detail="Column not found")
        
    # Check permissions
    board = crud.get_board_by_id(db, board_id=db_column.board_id)
    if not board or board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    crud.delete_column(db, column_id=column_id)
    return {"message": "Column deleted"}
