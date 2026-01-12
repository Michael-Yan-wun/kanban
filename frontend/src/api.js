// 優先讀取環境變數 (Deployment)，否則使用 Localhost
const BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000') + '/api';

/**
 * 通用 Fetch 封裝
 * 自動帶入 Token, JSON Content-Type
 */
export async function apiFetch(endpoint, options = {}) {
    // 1. 準備 Headers
    const token = localStorage.getItem('kanban_token');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }

    // 2. 準備 Config
    const config = {
        ...options,
        headers
    };

    // 3. 發送請求
    const response = await fetch(`${BASE_URL}${endpoint}`, config);

    // 4. 重導向處理 (401 Unauthorized -> Login)
    if (response.status === 401) {
        localStorage.removeItem('kanban_token');
        localStorage.removeItem('kanban_user');
        // 簡單暴力轉址，或者讓 Router Guard 處理
        if (!window.location.pathname.includes('/login')) {
            window.location.href = '/login';
        }
    }

    // 5. 解析回應
    // 若狀態碼不是 2xx，拋出錯誤
    if (!response.ok) {
        let errorMsg = response.statusText;
        try {
            const errorData = await response.json();
            errorMsg = errorData.detail || errorMsg;
        } catch (e) {
            // ignore JSON parse error
        }
        throw new Error(errorMsg);
    }

    // 若是 204 No Content，回傳 null
    if (response.status === 204) return null;

    return response.json();
}
