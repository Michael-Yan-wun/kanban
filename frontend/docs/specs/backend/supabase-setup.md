# Supabase 設定指南

## 📋 概述

本文檔說明如何在 Supabase 上建立 Kanban App 所需的資料庫。

---

## 🚀 Step 1: 建立 Supabase 專案

### 1.1 註冊/登入

1. 前往 [https://supabase.com](https://supabase.com)
2. 點擊 **Start your project**
3. 使用 GitHub 帳號登入（建議）

### 1.2 建立新專案

1. 點擊 **New Project**
2. 填寫專案資訊：
   - **Name**: `kanban-app` (或任意名稱)
   - **Database Password**: 設定一個強密碼 (**請記住！**)
   - **Region**: 選擇離你最近的區域 (例如：Southeast Asia - Singapore)
3. 點擊 **Create new project**
4. 等待約 2 分鐘讓專案初始化

---

## 🗄️ Step 2: 建立資料表

### 2.1 開啟 SQL Editor

1. 在左側選單點擊 **SQL Editor**
2. 點擊 **+ New query**

### 2.2 執行 Schema SQL

1. 複製 [database-schema.md](./database-schema.md) 中的「完整 SQL Schema」區塊
2. 貼到 SQL Editor 中
3. 點擊 **Run** (或按 Cmd/Ctrl + Enter)
4. 確認執行成功（應該看到綠色勾勾）

### 2.3 驗證資料表

1. 點擊左側 **Table Editor**
2. 應該看到 5 個資料表：
   - `users`
   - `boards`
   - `board_members`
   - `columns`
   - `tickets`

---

## 🔑 Step 3: 取得 API 金鑰

### 3.1 取得連線資訊

1. 點擊左側 **Project Settings** (齒輪圖示)
2. 點擊 **API**
3. 記錄以下資訊：

```
Project URL: https://xxxxxxxx.supabase.co
API Key (anon/public): eyJhbGciOiJIUzI1NiIsInR5cCI6...
API Key (service_role): eyJhbGciOiJIUzI1NiIsInR5cCI6... (後端使用，保密！)
```

### 3.2 取得資料庫連線字串

1. 點擊 **Database**
2. 往下滾動找到 **Connection string**
3. 選擇 **URI** 格式
4. 複製連線字串（記得替換 `[YOUR-PASSWORD]`）

```
postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
```

---

## ⚙️ Step 4: 設定環境變數

在後端專案中建立 `.env` 檔案：

```env
# 資料庫連線 (給 SQLAlchemy 使用)
# 格式: postgresql://[user]:[password]@[host]:[port]/[db]
DATABASE_URL=postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres

# API 連線 (如果需要直接呼叫 Supabase API)
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6... # service_role key

# Auth 設定 (Simple Token 字串長度)
TOKEN_LENGTH=64
```

> ⚠️ **重要**：`.env` 檔案不應該 commit 到 Git！請加入 `.gitignore`。
> 使用 `uv` 時，可以透過 `uv run` 自動讀取環境變數（需安裝 python-dotenv）。

---

## 📊 Step 5: 插入測試資料

### 5.1 使用 SQL Editor

```sql
-- 插入測試用戶
-- 注意：以下密碼 hash 是範例，實際使用時需要用 bcrypt 產生
-- admin123 -> $2b$12$...
-- user123 -> $2b$12$...

INSERT INTO users (username, password_hash, name, email, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.R5Z5z5z5z5z5z5', '系統管理員', 'admin@example.com', 'admin'),
('user1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.R5Z5z5z5z5z5z5', '張小明', 'user1@example.com', 'user'),
('user2', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.R5Z5z5z5z5z5z5', '李小華', 'user2@example.com', 'user');

-- 取得 user IDs
-- SELECT id, username FROM users;

-- 插入測試看板 (請替換 UUID)
-- INSERT INTO boards (name, description, owner_id) VALUES
-- ('產品開發', 'Q1 產品功能規劃', 'admin-uuid-here');
```

### 5.2 驗證資料

1. 在 **Table Editor** 中點擊 `users` 表
2. 確認有 3 筆測試用戶資料

---

## 🔒 Step 6: 安全設定 (可選)

### 6.1 關閉匿名存取

如果使用 FastAPI 自行管理驗證，建議：

1. 進入 **Authentication** > **Providers**
2. 關閉 **Email** 以外的所有 providers
3. 或者完全使用 **service_role** key 在後端操作

### 6.2 Row Level Security

如果需要啟用 RLS，參考 [database-schema.md](./database-schema.md) 中的 RLS 政策章節。

---

## ✅ 完成檢查清單

- [ ] Supabase 專案建立完成
- [ ] 5 個資料表建立完成 (users, boards, board_members, columns, tickets)
- [ ] 記錄 Project URL
- [ ] 記錄 API Key (anon)
- [ ] 記錄 API Key (service_role)
- [ ] 記錄 Database Password
- [ ] 建立後端 .env 檔案
- [ ] 測試資料插入完成 (可選)

---

## 🔗 相關資源

- [Supabase 官方文檔](https://supabase.com/docs)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [FastAPI + Supabase 教學](https://supabase.com/docs/guides/getting-started/quickstarts/python)

---

## 📝 下一步

資料庫設定完成後，繼續建立 FastAPI 後端：

1. 建立 FastAPI 專案結構
2. 設定 SQLAlchemy ORM
3. 實作 CRUD API
4. 實作 JWT 驗證
