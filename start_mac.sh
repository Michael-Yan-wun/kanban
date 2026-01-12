#!/bin/bash

# 定義顏色
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 正在啟動 Kanban App 全端開發環境...${NC}"

# 1. 啟動後端 (在背景執行)
echo -e "${GREEN}📦 啟動 Backend (FastAPI)...${NC}"
cd backend
uv run uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# 等待幾秒確保後端啟動
sleep 2

# 2. 啟動前端 (在前台執行)
echo -e "${GREEN}🎨 啟動 Frontend (Vite)...${NC}"
cd frontend
npm run dev

# 當前端被關閉 (Ctrl+C) 時，自動殺死後端程序
trap "kill $BACKEND_PID" EXIT
