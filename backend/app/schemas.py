from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# =======================
# Common
# =======================
class UserBase(BaseModel):
    username: str
    name: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class UserPasswordReset(BaseModel):
    password: str

# =======================
# Ticket Schemas
# =======================
class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None

class TicketCreate(TicketBase):
    board_id: int
    column_id: int

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    column_id: Optional[int] = None # 用於移動
    position: Optional[int] = None

class TicketResponse(TicketBase):
    id: int
    board_id: int
    column_id: int
    position: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# =======================
# Column Schemas
# =======================
class ColumnBase(BaseModel):
    name: str
    color: Optional[str] = "slate"

class ColumnCreate(ColumnBase):
    board_id: int
    position: Optional[int] = 0

class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    position: Optional[int] = None

class ColumnResponse(ColumnBase):
    id: int
    board_id: int
    position: int
    model_config = ConfigDict(from_attributes=True)

# =======================
# Board Schemas
# =======================
class BoardBase(BaseModel):
    name: str
    description: Optional[str] = None

class BoardCreate(BoardBase):
    pass

class BoardResponse(BoardBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    # 關聯資料 (Optional，視需要載入)
    columns: List[ColumnResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class BoardDetailResponse(BoardResponse):
    tickets: List[TicketResponse] = []
