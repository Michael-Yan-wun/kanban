import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiFetch } from '../api'

export const useUserStore = defineStore('user', () => {
    // ===== State =====
    const users = ref([])

    // ===== Getters =====
    const allUsers = computed(() => users.value)
    const userCount = computed(() => users.value.length)
    const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)

    // ===== Actions =====
    async function fetchUsers() {
        try {
            const data = await apiFetch('/users/')
            users.value = data
        } catch (error) {
            console.error('Fetch users failed:', error)
        }
    }

    function getUserById(userId) {
        return users.value.find(u => u.id === userId)
    }

    async function createUser(data) {
        try {
            const newUser = await apiFetch('/users/', {
                method: 'POST',
                body: JSON.stringify(data)
            })
            users.value.push(newUser)
            return { success: true, user: newUser }
        } catch (error) {
            console.error('Create user failed:', error)
            return { success: false, message: error.message || '新增失敗' }
        }
    }

    async function updateUser(userId, data) {
        try {
            const updatedUser = await apiFetch(`/users/${userId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            })
            const idx = users.value.findIndex(u => u.id === userId)
            if (idx !== -1) {
                users.value[idx] = updatedUser
            }
            return { success: true, user: updatedUser }
        } catch (error) {
            console.error('Update user failed:', error)
            return { success: false, message: error.message || '更新失敗' }
        }
    }

    async function deleteUser(userId) {
        // 前端預先檢查: 不允許刪除最後一個 admin (雖然前端沒法準確知道，但可以作為第一道防線或提示)
        const user = users.value.find(u => u.id === userId)
        if (user?.role === 'admin' && adminCount.value <= 1) {
            return { success: false, message: '無法刪除最後一個管理員' }
        }

        try {
            await apiFetch(`/users/${userId}`, {
                method: 'DELETE'
            })
            users.value = users.value.filter(u => u.id !== userId)
            return { success: true }
        } catch (error) {
            console.error('Delete user failed:', error)
            return { success: false, message: error.message || '刪除失敗' }
        }
    }

    async function resetPassword(userId, newPassword) {
        try {
            await apiFetch(`/users/${userId}/reset_password`, {
                method: 'POST',
                body: JSON.stringify({ password: newPassword })
            })
            return { success: true }
        } catch (error) {
            console.error('Reset password failed:', error)
            return { success: false, message: error.message || '重設密碼失敗' }
        }
    }

    return {
        // State
        users,
        // Getters
        allUsers,
        userCount,
        adminCount,
        // Actions
        fetchUsers,
        getUserById,
        createUser,
        updateUser,
        deleteUser,
        resetPassword
    }
})
