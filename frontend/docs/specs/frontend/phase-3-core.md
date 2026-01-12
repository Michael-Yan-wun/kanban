# Phase 3: 核心功能 - 登入、彈窗與看板 (UI)

## 📖 本階段作用
我們要製作第一個能互動的畫面。包含酷炫的登入頁面、通用的彈窗組件，以及最核心的「任務看板」。目前資料皆來自 Store 的 Mock Data。

## 🎯 目標
- 製作 `LoginView.vue` 與登入邏輯。
- 製作 `Modal.vue` 與 `TicketModal.vue`。
- 製作看板細節頁 `BoardDetailView.vue` (支援拖拉與編輯)。

---

## 🚀 實作指令 (直接複製給 AI)

```text
這是我專案的核心，請幫我使用 Vue 3 與 Tailwind CSS 實作 Kanban 核心 UI：

1. **`src/components/Modal.vue`**：
   - 通用彈窗，支援 Slot。
   - 樣式：`bg-slate-800`, `rounded-2xl`, 背景磨砂玻璃。

2. **`src/components/TicketModal.vue`**：
   - 專用於新增/編輯任務。
   - 欄位：標題、描述、優先級 (High/Medium/Low)、**開始時間**、**結束時間**。
   - **關鍵邏輯**:
     - `watch` props ticket：
       - 來源可能是 `start_date` (Mock) 或 `startDate` (Form)，需做相容處理。
     - `emit('save', data)`：送出的 data 統一使用前端慣用的 `startDate` / `dueDate`。

3. **`src/views/BoardDetailView.vue`**：
   - **排版**：滿版畫面，看板區域使用 `flex gap-6 overflow-x-auto`。
   - **拖拉互動**：使用 `<draggable>`。
   - **任務卡片 (Ticket Card)**：
     - 顯示標題、描述、優先級。
     - **顯示截止日期**：讀取 `ticket.due_date` (注意是 snake_case)。
     - Hover 效果與光暈。
   - **操作邏輯**:
     - `saveTicket`, `deleteTicket` 直接呼叫 Store actions (同步操作 Mock)。
     - 不需要 Loading Spinner (因為 Mock 很快)。

請輸出這些檔案的程式碼，確保風格極度高科技且具有層次感。
```

---

## ✅ 完成後的樣子
- 進入 `/login` 可以成功登入並跳轉。
- 進入 `/board/1` 可以看到漂亮的任務卡片，且可以左右拖拉。
- 點擊卡片可以編輯日期，且介面會立即更新 (因為是響應式 Store)。
