@echo off
echo ==========================================
echo 🚀 Starting Kanban App (Full Stack)
echo ==========================================

REM 1. 啟動後端 (開啟新視窗)
echo 📦 Launching Backend...
start "Kanban Backend" cmd /k "cd backend && uv run uvicorn app.main:app --reload --port 8000"

REM 等待 2 秒
timeout /t 2 /nobreak >nul

REM 2. 啟動前端 (開啟新視窗)
echo 🎨 Launching Frontend...
start "Kanban Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Services started in separate windows.
echo    - Backend: http://127.0.0.1:8000
echo    - Frontend: http://localhost:5173
echo.
pause
