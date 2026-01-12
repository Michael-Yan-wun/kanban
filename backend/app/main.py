from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, boards, columns, tickets, users
from .database import engine, Base

# 自動建立資料表 (若不存在)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kanban API", version="1.0.0")

# 設定 CORS (允許前端存取)
origins = [
    "http://localhost:5173", # Vite Default
    "http://127.0.0.1:5173",
    "*" # 開發階段先全開
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(boards.router, prefix="/api/boards", tags=["boards"])
app.include_router(columns.router, prefix="/api/columns", tags=["columns"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["tickets"])

@app.get("/")
def read_root():
    return {"message": "Kanban API is running 🚀"}
