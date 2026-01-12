from sqlalchemy import Column, Integer, String, Text, ForeignKey, BigInteger, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    role = Column(String(20), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tokens = relationship("AuthToken", back_populates="user", cascade="all, delete-orphan")
    owned_boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")

class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id = Column(BigInteger, primary_key=True, index=True)
    token = Column(String(64), unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tokens")

class Board(Base):
    __tablename__ = "boards"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="owned_boards")
    columns = relationship("KanbanColumn", back_populates="board", cascade="all, delete-orphan", order_by="KanbanColumn.position")
    tickets = relationship("Ticket", back_populates="board", cascade="all, delete-orphan")

class KanbanColumn(Base):
    __tablename__ = "columns"

    id = Column(BigInteger, primary_key=True, index=True)
    board_id = Column(BigInteger, ForeignKey("boards.id"), nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(String(20), default="slate")
    position = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    board = relationship("Board", back_populates="columns")
    tickets = relationship("Ticket", back_populates="column", cascade="all, delete-orphan")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(BigInteger, primary_key=True, index=True)
    board_id = Column(BigInteger, ForeignKey("boards.id"), nullable=False)
    column_id = Column(BigInteger, ForeignKey("columns.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default="medium")
    start_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    position = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    board = relationship("Board", back_populates="tickets")
    column = relationship("KanbanColumn", back_populates="tickets")
