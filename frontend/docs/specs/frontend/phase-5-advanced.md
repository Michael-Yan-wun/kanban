# Phase 5: 進階功能 - 統計圖表與管理後台 (Mock Data)

## 📖 本階段作用
這是專案最亮點的地方。我們要把資料視覺化，讓管理員能一眼看出各個專案的進度，並提供完整的用戶管理介面。資料目前來自 Mock Stores。

## 🎯 目標
- 實作 `AdminDashboardView.vue` (統計儀表板)。
- 實作 `UserManagementView.vue` (用戶 CRUD - Mock)。
- 使用 `Chart.js` 繪製圖表。

---

## 🚀 實作指令 (直接複製給 AI)

```text
這是我專案的最後一個開發階段：管理員統計儀表板與用戶管理。
請基於目前的 Mock Stores 進行開發：

1. **`src/views/AdminDashboardView.vue` (儀表板)**：
   - 使用 `Chart.js` 繪製 Doughnut (狀態分佈) 與 Bar (優先級)。
   - **統計邏輯**:
     - 讀取 `ticketStore.allTickets` (Mock Data)。
     - 依據 `ticket.column_id` 與 `column.board_id` 關聯，計算任務狀態。
     - **判定 "Done"**：每個 Board 中 position 最大的 Column 為「完成」欄位。
   - 視覺：四張大數字卡片 (Total Boards, Tasks, Users, Completion Rate) + 深色圖表卡片 (磨砂玻璃質感)。

2. **`src/views/UserManagementView.vue` (用戶管理)**：
   - 使用 `userStore` 提供的 Mock Data。
   - **Table 欄位**: Username, Name, Email, Role, CreatedAt, Actions.
   - **CRUD 與 Modal**:
     - 新增/編輯 Modal: 設定 Username, Password, Name, Email, Role。
     - 刪除: 需有確認 Modal。
     - 呼叫 Store 的同步 actions (如 `createUser` push 到 mock array)。

3. **`src/stores/userStore.js` (如果尚未完成)**：
   - 確保包含 `createUser`, `updateUser`, `deleteUser` 等操作 Mock Array 的功能。

請提供這兩個 Vue 檔案的完整代碼，確保圖表能正確渲染出 Store 裡的假資料。
```

---

## ✅ 完成後的樣子
- **Dashboard**: 可以看到漂亮的圖表，數據反映了 `mockData.js` 的內容。
- **User Management**: 可以新增/刪除假用戶，列表會即時更新。
