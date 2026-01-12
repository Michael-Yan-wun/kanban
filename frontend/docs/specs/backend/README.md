# 後端 Specs - FastAPI + Supabase (Simple Auth)

## 📖 概述

後端使用 **FastAPI** 框架，搭配 **Supabase** (PostgreSQL) 雲端資料庫。
驗證機制採用 **Simple Token Auth** (類似 Django Token)，適合快速開發與小型專案。

---

## 📋 文件總覽

| 文件 | 說明 | 用途 |
|------|------|------|
| [supabase-setup.md](./supabase-setup.md) | Supabase 設定指南 | 建立雲端資料庫 |
| [database-schema.md](./database-schema.md) | 資料庫結構設計 | SQL Schema (Simple Token 版) |
| *(待新增)* | FastAPI + uv 專案架構 | 使用 uv 初始化專案 |
| *(待新增)* | Token Auth API | 登入、登出與權限檢查 |

---

## 🚀 快速開始 (使用 uv)

我們推薦使用 [uv](https://github.com/astral-sh/uv) 進行 Python 專案管理，這比 pip 快非常多且更簡潔。

### Step 1: 設定資料庫
1. 參照 [supabase-setup.md](./supabase-setup.md) 建立 Supabase 專案。
2. 在 SQL Editor 執行 [database-schema.md](./database-schema.md) 的內容。

### Step 2: 初始化後端專案
```bash
# 安裝 uv (如果還沒安裝)
curl -LsSf https://astral-sh.uv.install.sh | sh

# 建立專案目錄
mkdir kanban-backend && cd kanban-backend

# 使用 uv 初始化
uv init

# 安裝基本依賴
uv add fastapi uvicorn sqlalchemy psycopg2-binary passlib bcrypt

# 啟動開發伺服器
uv run uvicorn main:app --reload
```

---

## 🛠️ 技術棧

| 技術 | 用途 |
|------|------|
| **uv** | 專案與依賴管理 (Next-gen) |
| **FastAPI** | 高性能 Web 框架 |
| **SQLAlchemy** | ORM 資料庫操作 |
| **Simple Token** | 簡易認證機制 (標頭: Authorization: Token xxx) |
| **passlib + bcrypt** | 密碼雜湊安全存儲 |
| **Supabase** | 雲端 PostgreSQL |

---

## � 認證邏輯 (Simple Token)

1. **登入**: 前端發送帳密，後端比對成功後，在 `auth_tokens` 表產生一組隨機 String 並返回。
2. **請求**: 前端將 Token 存於 LocalStorage，之後請求帶上 `Authorization: Token <key>`。
3. **驗證**: 後端 Middleware 攔截請求，去 DB 查這組 Token 對應的 User ID 以及 Role。
4. **權限**: 根據 User 的 `role` (admin/user) 決定是否允許操作。

---

## ✅ 完成檢查清單
- [ ] Supabase 專案建立
- [ ] 資料庫 Schema 執行 (含 auth_tokens 表)
- [ ] uv 環境建置完成
- [ ] 測試 Token 登入邏輯 (待新增)
- [ ] 前後端 Token 對接 (待新增)
