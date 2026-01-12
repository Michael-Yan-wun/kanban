# Deployment Guide (Zeabur)

本專案已優化為適合 **Zeabur** 一鍵部署的結構。請依照以下步驟進行部署。

## 1. 準備工作

確保你已經將最新程式碼推送到 GitHub：
- `backend/requirements.txt` 已建立 (由 `uv export` 產生)。
- `frontend/src/api.js` 已設定為讀取 `VITE_API_URL` 環境變數。

## 2. 資料庫設定 (Supabase)

因為本專案使用 **Supabase** 作為外部資料庫，你不需要在 Zeabur 上建立資料庫服務。

1. **取得連線字串**:
   - 登入 Supabase Dashboard -> Project Settings -> Database -> Connection String (URI).
   - 確保使用 `Production` 模式的連線字串 (Port 5432 或 6543 均可，建議 5432)。
   - 格式範例：`postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres`

2. **準備環境變數**:
   - 等一下部署後端時，我們會將此字串填入 `DATABASE_URL`。

## 3. 部署後端 (Backend)

1. 建立 **Git Service**，選擇本專案的 Repo。
2. 選取 **backend** 作為服務名稱 (或由 Zeabur 自動偵測)。
3. **Settings (設定)**:
   - **Root Directory**: `backend`
   - **Watch Paths**: `backend` (Optional)
4. **Environment Variables (環境變數)**:
   - `DATABASE_URL`: 貼上剛剛複製的 PostgreSQL 連線字串。
   - `SECRET_KEY`: 設定一個隨機的長字串 (如 `vibe-coding-secret-123`)。
   - `CORS_ORIGINS`: 若部署後前端無法連線，可設為 `*` 或前端網址。
5. **Networking**:
   - 開啟 **Public Networking**。
   - 複製生成的網址 (例如 `https://kanban-backend.zeabur.app`)。

> **注意**: 因為我們使用了 `uv`，如果 Zeabur 預設 Python Buildpack 跑不動，切換到部署設定，確認它有讀取到 `requirements.txt`。通常 Zeabur 會自動處理。

## 4. 部署前端 (Frontend)

1. 在同一個專案中，再建立一個 **Git Service** (連結同一個 Repo)。
2. 選取 **frontend**。
3. **Settings (設定)**:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Output Directory**: `dist`
4. **Environment Variables (環境變數)**:
   - `VITE_API_URL`: 填入 **後端網址** (除去結尾的 `/`)。
     - 例如: `https://kanban-backend.zeabur.app`
     - **注意**: 不要加 `/api`，程式碼會自動串接。
5. **Networking**:
   - 開啟 **Public Networking**。
   - 這就是你的最終網址！

## 5. 初始化資料庫 (Advanced)

部署後端後，資料庫是空的。Zeabur 通常支援在 Web Shell 中執行指令。
進入 Backend 服務的 **Console** 頁籤，執行：

```bash
# 執行日期欄位遷移
python verify_api.py  # 或手動觸發 migrate logic
```

(或者如果你有 `migrate.py`，可以直接執行 `python migrate.py`)。

---

## 常見問題

- **前端顯示 Network Error**: 檢查 `VITE_API_URL` 是否正確，以及後端是否允許了 CORS。
- **後端 Deploy Failed**: 檢查 `requirements.txt` 是否存在，或 `python` 版本設定。
