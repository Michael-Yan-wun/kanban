# Phase 1: 專案架構與環境初始化

## 📖 本階段作用
這是專案的「地基」。我們會建立一個 Vue 3 專案，裝好所有需要的工具（如排版用的 Tailwind、跳轉頁面的 Router），並設定好一個酷炫的深色風格。

## 🎯 目標
- 初始化 Vue 3 + Vite 專案
- 設定 Tailwind CSS 深色主題
- 建立基礎資料夾結構與路由位址

---

## 🚀 實作指令 (直接複製給 AI)

```text
請幫我初始化一個 Vue 3 (Vite) 前端專案，並嚴格遵守以下開發規格：

1. **依賴安裝**：`npm install vue-router pinia tailwindcss postcss autoprefixer lucide-vue-next vuedraggable@next chart.js vue-chartjs`。

2. **入口設定 (`src/main.js`)**：
   - 務必引入並使用 `createPinia()` 和 `router`。
   - 引入 `./style.css`。

3. **Tailwind 全域樣式 (`src/style.css`)**：
   - 背景使用：`bg-[#0f172a]` (深藍黑)。
   - 字體使用：'Inter', sans-serif。
   - 自定義滾動條：寬度 6px，軌道透明，滑塊為 `slate-700` 圓角。
   - 基本卡片樣式：`@apply bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl;`。

4. **路由規格 (`src/router/index.js`)**：
   - 使用 `createWebHistory`。
   - 包含路徑：`/login`, `/boards`, `/board/:id`, `/admin`。
   - **路由守衛**：檢查 `localStorage.getItem('kanban_token')`。除了 `/login` 之外，其餘頁面若無 token 則 redirect 到 `/login`。

5. **App.vue**：
   - 清空預設內容，僅保留 `<router-view />`。
   - 確保根元素有 `min-h-screen text-slate-200`。

請產出 main.js, vite.config.js, style.css, router/index.js, App.vue 的完整代碼。
```

---

## ✅ 完成後的樣子
- 執行 `npm run dev` 網頁會出現，且背景是深色的。
- 切換網址（如 `/login`）不會出錯。
