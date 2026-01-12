import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiFetch } from '../api'

export const useBoardStore = defineStore('board', () => {
    const allBoards = ref([])
    const currentBoard = ref(null)

    // Actions
    async function fetchBoards() {
        try {
            const data = await apiFetch('/boards/')
            allBoards.value = data
        } catch (error) {
            console.error('Failed to fetch boards:', error)
        }
    }

    async function fetchBoardDetail(boardId) {
        try {
            const data = await apiFetch(`/boards/${boardId}`)
            currentBoard.value = data
            return data
        } catch (error) {
            console.error('Failed to fetch board detail:', error)
            throw error
        }
    }

    async function createBoard(name) {
        try {
            const newBoard = await apiFetch('/boards/', {
                method: 'POST',
                body: JSON.stringify({ name })
            })
            allBoards.value.push(newBoard)
            return newBoard
        } catch (error) {
            console.error('Create board failed:', error)
            throw error
        }
    }

    // Helper: 透過 ID 取得本地緩存的 Board (不打 API)
    const getBoardById = (id) => allBoards.value.find(b => b.id === Number(id))

    return {
        allBoards,
        currentBoard,
        fetchBoards,
        fetchBoardDetail,
        createBoard,
        getBoardById
    }
})
