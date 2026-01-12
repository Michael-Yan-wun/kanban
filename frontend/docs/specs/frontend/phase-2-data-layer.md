# Phase 2: 資料層與狀態管理 (Pinia + Mock Data)

## 📖 本階段作用
這是 App 的「大腦」。在後端完成之前，我們先用「假資料」來讓網頁動起來。
**關鍵策略**：為了讓未來串接後端時不用大改 UI，我們的 Mock Data 欄位名稱將預先採用後端慣用的 `snake_case` (如 `board_id`, `start_date`)。

## 🎯 目標
- 建立 `mockData.js`。
- 實作 `authStore`, `boardStore`, `columnStore`, `ticketStore`, `userStore`。
- 實現純前端的 CRUD (重整頁面後資料會重置是正常的，除非存 LocalStorage)。

---

## 🚀 實作指令 (直接複製給 AI)

```text
請幫我開發 Vue 3 專案的資料層 (Pinia Stores)，使用 Setup Syntax。
目前尚未有後端，請使用 **Mock Data** 模擬所有運作。

1. **`src/stores/mockData.js`**：
   - 匯出 `mockUsers`, `mockBoards`, `mockColumns`, `mockTickets`。
   - **重要命名規則** (為了未來整合)：
     - ID 欄位請用 `board_id`, `column_id` (Snake Case)。
     - 日期欄位請用 `start_date`, `due_date`, `created_at` (Snake Case)。
   - **Ticket 資料範例**：
     ```js
     { id: 101, board_id: 1, column_id: 1, title: "設計首頁", priority: "high", start_date: "2023-10-01", due_date: "2023-10-05" }
     ```

2. **`src/stores/authStore.js`**：
   - `login(username, password)`: 比對 mockUsers。成功則存入 LocalStorage。

3. **`src/stores/boardStore.js`**：
   - `fetchBoards()`: 回傳 `mockBoards`。
   - `createBoard(name)`: Push 到 `mockBoards` 陣列。

4. **`src/stores/columnStore.js`**：
   - `fetchColumns(boardId)`: 從 `mockColumns` 過濾 `c.board_id === boardId`。
   - `createColumn`: 新增並自動計算 `position`。

5. **`src/stores/ticketStore.js`**：
   - `fetchTickets(boardId)`: 從 `mockTickets` 過濾 `t.board_id === boardId`。
   - `createTicket(data)`: 接收 `startDate`, `dueDate` (CamelCase)，存入 Mock Data 時轉為 `start_date`, `due_date`。
   - `updateTicket`, `deleteTicket`: 操作 Mock 陣列。

6. **`src/stores/userStore.js`**：
   - `fetchUsers()`: 回傳 `mockUsers`。
   - `createUser`, `updateUser`...: 操作 Mock 陣列。

請提供這些檔案的完整代碼，確保前端功能完全可用。
```

---

## ✅ 完成後的樣子
- 使用 Vue Devtools 可以看到 Stores 裡填滿了假資料。
- 雖然沒有後端，但新增看板、移動卡片都能在畫面上運作 (重整後消失沒關係)。
