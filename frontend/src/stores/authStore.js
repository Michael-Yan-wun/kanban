import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiFetch } from '../api'

export const useAuthStore = defineStore('auth', () => {
    // ===== State =====
    const token = ref(localStorage.getItem('kanban_token') || null)
    // 嘗試從 localStorage 恢復 user 物件
    const storedUser = localStorage.getItem('kanban_user')
    const user = ref(storedUser ? JSON.parse(storedUser) : null)

    // ===== Getters =====
    const isLoggedIn = computed(() => !!token.value)
    const isAdmin = computed(() => user.value?.role === 'admin')
    const currentUser = computed(() => user.value)

    // ===== Actions =====
    async function login(username, password) {
        try {
            // 1. 取得 Token
            const data = await apiFetch('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ username, password })
            })

            token.value = data.access_token
            // user 資訊後端也有回傳
            user.value = data.user

            // 2. 存入 LocalStorage
            localStorage.setItem('kanban_token', token.value)
            localStorage.setItem('kanban_user', JSON.stringify(user.value))

            return { success: true }
        } catch (error) {
            console.error('Login failed:', error)
            return { success: false, message: error.message }
        }
    }

    function logout() {
        token.value = null
        user.value = null
        localStorage.removeItem('kanban_token')
        localStorage.removeItem('kanban_user')
        window.location.href = '/login'
    }

    // 初始化驗證 (Optional: 每次 reload 可呼叫 /auth/me 確認 token 有效性)
    async function checkAuth() {
        if (!token.value) return
        try {
            const userData = await apiFetch('/auth/me')
            user.value = userData
            localStorage.setItem('kanban_user', JSON.stringify(userData))
        } catch (e) {
            logout()
        }
    }

    return {
        token,
        user,
        isLoggedIn,
        isAdmin,
        currentUser,
        login,
        logout,
        checkAuth
    }
})
