# Kanban App - Spec 文件總覽

## 📁 目錄結構

```
docs/specs/
├── README.md                    # 本文件
├── frontend/                    # 前端 Specs (Vue 3)
│   ├── README.md                # 前端教學指南
│   ├── phase-1-foundation.md    # 專案架構
│   ├── phase-2-data-layer.md    # 資料層 (Pinia)
│   ├── phase-3-core.md          # 核心功能
│   ├── phase-4-multiboard.md    # 多看板與導航
│   └── phase-5-advanced.md      # 進階功能
└── backend/                     # 後端 Specs (FastAPI)
    ├── database-schema.md       # 資料庫結構設計
    ├── supabase-setup.md        # Supabase 設定指南
    └── (更多 specs 待新增...)
```

---

## 🎯 學習路徑

### 前端 (Vue 3 + Vite + Pinia)

1. 閱讀 [frontend/README.md](./frontend/README.md)
2. 依序完成 Phase 1 ~ Phase 5
3. 預估時間：**3.5 - 4 小時**

### 後端 (FastAPI + Supabase)

1. 閱讀 [backend/supabase-setup.md](./backend/supabase-setup.md) 設定資料庫
2. 參考 [backend/database-schema.md](./backend/database-schema.md) 了解資料結構
3. 依序完成後端 Phases (待新增)
4. 預估時間：**TBD**

---

## 🛠️ 技術棧

| 層級 | 技術 |
|------|------|
| **前端** | Vue 3, Vite, Pinia, Vue Router, TailwindCSS, vuedraggable |
| **後端** | FastAPI, SQLAlchemy, Pydantic, JWT |
| **資料庫** | Supabase (PostgreSQL) |

---

## ✅ 完成檢查清單

### 前端
- [ ] Phase 1: 專案架構
- [ ] Phase 2: 資料層
- [ ] Phase 3: 核心功能  
- [ ] Phase 4: 多看板與導航
- [ ] Phase 5: 進階功能

### 後端
- [ ] Supabase 資料庫設定
- [ ] FastAPI 專案架構 (待新增)
- [ ] CRUD API (待新增)
- [ ] JWT 驗證 (待新增)
- [ ] 前後端整合 (待新增)
