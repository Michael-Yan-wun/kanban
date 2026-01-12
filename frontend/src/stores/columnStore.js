import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiFetch } from '../api'

export const useColumnStore = defineStore('column', () => {
    // 簡單設計：我們把所有看過的 columns 都存在這裡，或者只存當前 board 的
    // 為了簡單，我們維護一個 Map: boardId -> columns[]
    // 但 state 必須單純，所以用單一陣列 + filter
    const columns = ref([])

    async function fetchColumns(boardId) {
        try {
            const data = await apiFetch(`/columns/?board_id=${boardId}`)
            // 更新本地 Store: 先移除該 board 舊資料，再加入新資料
            // 這裡簡單做法：把非此 board 的留著，加上新的
            // Note: API returns snake_case 'board_id'
            const otherBoardCols = columns.value.filter(c => c.board_id !== Number(boardId))
            columns.value = [...otherBoardCols, ...data]
            return data
        } catch (error) {
            console.error('Fetch columns failed:', error)
        }
    }

    async function createColumn({ boardId, name, color = 'slate' }) {
        try {
            const newCol = await apiFetch('/columns/', {
                method: 'POST',
                body: JSON.stringify({ board_id: boardId, name, color })
            })
            columns.value.push(newCol)
            return newCol
        } catch (error) {
            console.error('Create column failed:', error)
            throw error
        }
    }

    async function updateColumn(columnId, updates) {
        try {
            const updatedCol = await apiFetch(`/columns/${columnId}`, {
                method: 'PUT',
                body: JSON.stringify(updates)
            })
            // Update local state
            const index = columns.value.findIndex(c => c.id === Number(columnId))
            if (index !== -1) {
                columns.value[index] = updatedCol
            }
            return updatedCol
        } catch (error) {
            console.error('Update column failed:', error)
            throw error
        }
    }

    async function deleteColumn(columnId) {
        try {
            await apiFetch(`/columns/${columnId}`, {
                method: 'DELETE'
            })
            // Update local state
            columns.value = columns.value.filter(c => c.id !== Number(columnId))
        } catch (error) {
            console.error('Delete column failed:', error)
            throw error
        }
    }

    // Getters
    const getColumnsByBoard = (boardId) => {
        return columns.value
            .filter(c => (c.board_id === Number(boardId) || c.boardId === Number(boardId)))
            .sort((a, b) => a.position - b.position)
    }

    return {
        columns,
        fetchColumns,
        createColumn,
        updateColumn,
        deleteColumn,
        getColumnsByBoard
    }
})
