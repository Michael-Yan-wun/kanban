from sqlalchemy.orm import Session
from sqlalchemy import func
import bcrypt
from . import models, schemas
import secrets

def verify_password(plain_password: str, hashed_password: str):
    # bcrypt.checkpw 需要 bytes
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str):
    # bcrypt.hashpw 回傳 bytes，需要 decode 存入 string DB column
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# ====== Users ======
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # 強制更新時間
    db_user.updated_at = func.now()
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def reset_password(db: Session, user_id: int, new_password: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        hashed_password = get_password_hash(new_password)
        db_user.password_hash = hashed_password
        db_user.updated_at = func.now()
        db.commit()
        return True
    return False

# ====== Auth Tokens ======
def create_auth_token(db: Session, user_id: int):
    token_str = "token_" + secrets.token_hex(16)
    db_token = models.AuthToken(token=token_str, user_id=user_id)
    db.add(db_token)
    db.commit()
    return token_str

def get_user_by_token(db: Session, token: str):
    auth_token = db.query(models.AuthToken).filter(models.AuthToken.token == token).first()
    if auth_token:
        return auth_token.user
    return None

# ====== Boards ======
def get_boards(db: Session, user_id: int):
    # 簡單實作：只回傳自己擁有的，或者公開的 (這裡先只回傳 User 擁有的)
    return db.query(models.Board).filter(models.Board.owner_id == user_id).all()

def create_board(db: Session, board: schemas.BoardCreate, user_id: int):
    db_board = models.Board(**board.model_dump(), owner_id=user_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    
    # 自動建立預設欄位
    default_cols = ["Todo", "In Progress", "Done"]
    for idx, name in enumerate(default_cols):
        db_col = models.KanbanColumn(board_id=db_board.id, name=name, position=idx)
        db.add(db_col)
    db.commit()
    
    return db_board

def get_board_by_id(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.id == board_id).first()

# ====== Columns ======
def create_column(db: Session, column: schemas.ColumnCreate):
    db_column = models.KanbanColumn(**column.model_dump())
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column

def get_columns_by_board(db: Session, board_id: int):
    return db.query(models.KanbanColumn)\
        .filter(models.KanbanColumn.board_id == board_id)\
        .order_by(models.KanbanColumn.position.asc())\
        .all()

# ====== Tickets ======
def create_ticket(db: Session, ticket: schemas.TicketCreate):
    # 自動計算 Position (放在該欄位最後)
    max_pos = db.query(func.max(models.Ticket.position))\
        .filter(models.Ticket.column_id == ticket.column_id)\
        .scalar() or 0
    
    db_ticket = models.Ticket(**ticket.model_dump(), position=max_pos + 1)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_tickets_by_board(db: Session, board_id: int):
    return db.query(models.Ticket).filter(models.Ticket.board_id == board_id).all()

def update_ticket(db: Session, ticket_id: int, ticket_update: schemas.TicketUpdate):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        return None
    
    update_data = ticket_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)
    
    # 強制更新時間
    db_ticket.updated_at = func.now()
    
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def delete_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
    return db_ticket

# ====== More Board CRUD ======
def update_board(db: Session, board_id: int, board_update: schemas.BoardCreate):
    db_board = db.query(models.Board).filter(models.Board.id == board_id).first()
    if not db_board:
        return None
    for key, value in board_update.model_dump(exclude_unset=True).items():
        setattr(db_board, key, value)
    
    # 強制更新時間
    db_board.updated_at = func.now()

    db.commit()
    db.refresh(db_board)
    return db_board

def delete_board(db: Session, board_id: int):
    db_board = db.query(models.Board).filter(models.Board.id == board_id).first()
    if db_board:
        db.delete(db_board)
        db.commit()
    return db_board

# ====== More Column CRUD ======
def get_column(db: Session, column_id: int):
    return db.query(models.KanbanColumn).filter(models.KanbanColumn.id == column_id).first()

def update_column(db: Session, column_id: int, column_update: schemas.ColumnUpdate):
    db_column = db.query(models.KanbanColumn).filter(models.KanbanColumn.id == column_id).first()
    if not db_column:
        return None
    for key, value in column_update.model_dump(exclude_unset=True).items():
        setattr(db_column, key, value)
    
    # 強制更新時間
    db_column.updated_at = func.now()

    db.commit()
    db.refresh(db_column)
    return db_column

def delete_column(db: Session, column_id: int):
    db_column = db.query(models.KanbanColumn).filter(models.KanbanColumn.id == column_id).first()
    if db_column:
        db.delete(db_column)
        db.commit()
    return db_column
