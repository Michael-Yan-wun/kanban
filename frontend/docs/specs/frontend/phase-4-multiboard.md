# Phase 4: 導航系統與全域佈局

## 📖 本階段作用
讓使用者可以在不同看板之間輕鬆切換。我們會建立側邊欄與首頁的看板列表。

## 🎯 目標
- 實作 `Sidebar.vue` 元件。
- 實作 `BoardListView.vue` (所有的看板卡片)。
- 設定路由守衛（無 Token 不准進入看板）。

---

## 🚀 實作指令 (直接複製給 AI)

```text
這是我專案的導航層面，請幫我實作全域佈局與導航系統：

1. **`src/components/Sidebar.vue`**：
   - 垂直導航，`bg-slate-900/80`, `border-r border-slate-800`。
   - 頂部：App Logo (可以使用 Lucide 的 Layout 圖示)。
   - 中間：`v-for` 渲染 `boardStore.allBoards`。
   - 底部：設定 (`/admin`) 與登出按鈕。

2. **`src/views/BoardListView.vue`**：
   - 注意：`LoginView` 顯示時不應該出現 Sidebar。

3. **`src/App.vue` 佈局架構**：
   - 使用 `useRoute` 取得當前路由。
   - 邏輯：`const showSidebar = computed(() => route.name !== 'login')`。
   - Template：
     ```html
     <div class="flex min-h-screen bg-[#0f172a] text-slate-200">
       <Sidebar v-if="showSidebar" />
       <main class="flex-1 p-8 overflow-auto">
         <router-view />
       </main>
     </div>
     ```

4. **路由守衛 (Router Guard)**：
   - 在 `router/index.js` 使用 `router.beforeEach`。
   - 檢查：若 `to.name !== 'login'` 且 `!localStorage.getItem('kanban_token')`，則 `next({ name: 'login' })`。

請詳細說明如何實作這種佈局切換，並提供程式碼。
```

---

## ✅ 完成後的樣子
- 登入後，左側會出現側邊欄，可以切換看板。
- 未登入時直接輸入網址會被退回登入頁。
