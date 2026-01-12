from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import crud, schemas, deps
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.BoardResponse)
def create_board(
    board: schemas.BoardCreate,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_board(db=db, board=board, user_id=current_user.id)

@router.get("/", response_model=List[schemas.BoardResponse])
def read_boards(
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_boards(db=db, user_id=current_user.id)

@router.get("/{board_id}", response_model=schemas.BoardDetailResponse)
def read_board(
    board_id: int,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    board = crud.get_board_by_id(db, board_id=board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    # 簡單權限檢查：只有 owner 可以看 (或 member)
    # 這裡暫時只檢查 owner，實際專案應檢查 board_members
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return board

@router.put("/{board_id}", response_model=schemas.BoardResponse)
def update_board(
    board_id: int,
    board_update: schemas.BoardCreate,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    board = crud.get_board_by_id(db, board_id=board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    return crud.update_board(db, board_id=board_id, board_update=board_update)

@router.delete("/{board_id}")
def delete_board(
    board_id: int,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    board = crud.get_board_by_id(db, board_id=board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    crud.delete_board(db, board_id=board_id)
    return {"message": "Board deleted"}
