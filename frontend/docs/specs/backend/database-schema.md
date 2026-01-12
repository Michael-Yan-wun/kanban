# Kanban App - 資料庫設計文件 (精簡版)

## 📋 概述

本文件定義 Kanban App 的資料庫結構，使用 **Supabase** (PostgreSQL) 作為雲端資料庫。
所有主鍵皆使用 **Auto-increment Integer**。

---

## 📊 Table 定義

### 1. users (用戶)
| 欄位 | 類型 | 約束 | 說明 |
|------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 用戶 ID (1, 2, 3...) |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 登入帳號 |
| password_hash | VARCHAR(255) | NOT NULL | 密碼雜湊值 |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'user' | 角色 (admin/user) |

### 2. auth_tokens (認證 Token)
| 欄位 | 類型 | 約束 | 說明 |
|------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | Token ID |
| token | VARCHAR(64) | UNIQUE, NOT NULL | 隨機 Token |
| user_id | BIGINT | REFERENCES users(id) | 所屬用戶 |

### 3. boards (看板)
| 欄位 | 類型 | 約束 | 說明 |
|------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 看板 ID |
| name | VARCHAR(100) | NOT NULL | 名稱 |
| owner_id | BIGINT | REFERENCES users(id) | 擁有者 |

### 4. board_members (看板成員)
| 欄位 | 類型 | 約束 | 說明 |
|------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | |
| board_id | BIGINT | REFERENCES boards(id) | |
| user_id | BIGINT | REFERENCES users(id) | |

### 5. columns (欄位)
| 欄位 | 類型 | 約束 | 說明 |
|------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | |
| board_id | BIGINT | REFERENCES boards(id) | |
| name | VARCHAR(100) | NOT NULL | |
| position | INTEGER | DEFAULT 0 | 排序 |

### 6. tickets (任務)
| 欄位 | 類型 | 約束 | 說明 |
|------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | |
| column_id | BIGINT | REFERENCES columns(id) | |
| title | VARCHAR(255) | NOT NULL | |
| position | INTEGER | DEFAULT 0 | 排序 |

---

## 📝 完整 SQL Schema (一鍵執行版)

將以下 SQL 複製到 Supabase SQL Editor 執行：

```sql
-- =====================================================
-- Kanban App Database Schema
-- 適用於 Supabase (PostgreSQL)
-- 使用 Simple Token 驗證 | Auto-increment IDs
-- =====================================================

-- 1. 重置所有表 (開發階段使用，生產環境請勿執行)
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS columns CASCADE;
DROP TABLE IF EXISTS board_members CASCADE;
DROP TABLE IF EXISTS boards CASCADE;
DROP TABLE IF EXISTS auth_tokens CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. users 表
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. auth_tokens 表 (Simple Token 驗證)
CREATE TABLE auth_tokens (
    id BIGSERIAL PRIMARY KEY,
    token VARCHAR(64) UNIQUE NOT NULL,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. boards 表
CREATE TABLE boards (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. board_members 表 (中間表)
CREATE TABLE board_members (
    id BIGSERIAL PRIMARY KEY,
    board_id BIGINT NOT NULL REFERENCES boards(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member',
    UNIQUE(board_id, user_id)
);

-- 6. columns 表
CREATE TABLE columns (
    id BIGSERIAL PRIMARY KEY,
    board_id BIGINT NOT NULL REFERENCES boards(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(20) DEFAULT 'slate',
    position INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. tickets 表
CREATE TABLE tickets (
    id BIGSERIAL PRIMARY KEY,
    board_id BIGINT NOT NULL REFERENCES boards(id) ON DELETE CASCADE,
    column_id BIGINT NOT NULL REFERENCES columns(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    start_date TIMESTAMPTZ,
    due_date TIMESTAMPTZ,
    position INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- 自動更新 updated_at 的 Trigger
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_boards_updated_at ON boards;
CREATE TRIGGER update_boards_updated_at
    BEFORE UPDATE ON boards
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_columns_updated_at ON columns;
CREATE TRIGGER update_columns_updated_at
    BEFORE UPDATE ON columns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_tickets_updated_at ON tickets;
CREATE TRIGGER update_tickets_updated_at
    BEFORE UPDATE ON tickets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 🧪 測試資料 SQL

```sql
INSERT INTO users (username, password_hash, name, role) VALUES
('admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '系統管理員', 'admin'),
('user1', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '張小明', 'user');

INSERT INTO boards (name, description, owner_id) VALUES
('產品開發', 'Q1 專案追蹤', 1),
('行銷專案', '年度活動', 2);

INSERT INTO columns (board_id, name, color, position) VALUES
(1, '待辦事項', 'slate', 0), (1, '進行中', 'blue', 1), (1, '已完成', 'green', 2);

INSERT INTO tickets (board_id, column_id, title, priority) VALUES
(1, 1, '前端開發', 'medium'),
(1, 3, '設計 API', 'high');
```
