from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import crud, schemas, deps
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.TicketResponse)
def create_ticket(
    ticket: schemas.TicketCreate,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    # 權限檢查省略，邏輯同上
    return crud.create_ticket(db=db, ticket=ticket)

@router.get("/", response_model=List[schemas.TicketResponse])
def read_tickets(
    board_id: int,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_tickets_by_board(db, board_id=board_id)

@router.put("/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_update: schemas.TicketUpdate,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    ticket = crud.update_ticket(db, ticket_id=ticket_id, ticket_update=ticket_update)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    crud.delete_ticket(db, ticket_id=ticket_id)
    return {"message": "Ticket deleted"}
