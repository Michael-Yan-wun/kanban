# 🔌 前後端串接整合 (Integration - Final)

## 📖 概述
恭喜你！現在你已經擁有完整的 Vue 3 前端與 FastAPI 後端。我們要進行最後的深度整合，確保所有 CRUD、時間處理與用戶管理都能完美運作。

---

## 🚀 實作指令 (Prompt 範例)

### Prompt 1: 建立 API 連線層與 Auth
(同原計畫，確保 `apiFetch` 處理 401 自動登出)

### Prompt 2: 升級資料 Stores (完整 CRUD)

```text
請繼續升級以下 Stores，改用 `apiFetch` 並支援 **完整非同步操作 (Async/Await)**：

1. **`src/stores/boardStore.js`**：
   - Fetch: GET `/boards/`
   - Create: POST `/boards/`
   - Update: PUT `/boards/{id}`
   - Delete: DELETE `/boards/{id}`

2. **`src/stores/columnStore.js`**：
   - Fetch: GET `/columns/?board_id={id}` (注意 **snake_case**)
   - Create: POST `/columns/`
   - Update: PUT `/columns/{id}`
   - Delete: DELETE `/columns/{id}`

3. **`src/stores/ticketStore.js`**：
   - Fetch: GET `/tickets/?board_id={id}`
   - Create/Update: 支援 `start_date`, `due_date`。
     - 前端輸入為 `startDate`, `dueDate` (Camel Case)。
     - POST/PUT Payload轉為 `start_date`, `due_date` (Snake Case)。
   - Delete: DELETE `/tickets/{id}`

請提供更新後的 Stores，並確保所有寫入操作都 `await` API 回應。
```

### Prompt 3: 升級 View 層邏輯 (Loading & Errors)

```text
請修正 View 層，加入 Loading 狀態與錯誤處理：

1. **`src/views/BoardDetailView.vue`**:
   - 加入 `const isSubmitting = ref(false)`。
   - 所有按鈕 (新增/儲存/刪除) 在 `isSubmitting` 為 true 時應 disabled 並顯示 spinner。
   - 確保日期選擇器 (Start/End) 正確綁定並傳入 Store。

2. **`src/views/UserManagementView.vue`**:
   - `onMounted` 時呼叫 `await userStore.fetchUsers()`。
   - 表格欄位：Username, Name, Email, Role, CreatedAt。
   - 實作完整 CRUD Modal。
```

### Prompt 4: 後端 CRUD 補強 (Backend Fixes)

```text
確保後端邏輯正確處理邊界情況：

1. **`updated_at`**: 在 CRUD 的 Update 函數中，強制執行 `db_obj.updated_at = func.now()`，確保時間戳記更新。
2. **User API**: 確保 `routers/users.py` 存在並註冊於 `main.py`。
3. **Snake Case**: 確保 API 回傳的欄位名稱 (如 `board_id`, `column_id`) 與前端 Store 的預期一致。
```

---

## ✅ 串接後檢查清單 (Checklist)
- [ ] **Auth**: 登入/登出/Token失效導向。
- [ ] **Boards**: 列表顯示、新增、編輯、刪除 (Cascade Delete)。
- [ ] **Columns**: 拖拉排序、編輯名稱/顏色、刪除。
- [ ] **Tickets**: 
    - 拖拉移動 (跨欄位)。
    - 新增/編輯 (含 **開始/結束時間**)。
    - 刪除。
- [ ] **Users**: 列表顯示、CRUD 操作、重設密碼。
- [ ] **Admin Dashboard**: 統計圖表正確顯示 (無 "未分類" 錯誤)。
