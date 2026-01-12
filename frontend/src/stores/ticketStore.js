import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiFetch } from '../api'

export const useTicketStore = defineStore('ticket', () => {
    const allTickets = ref([])

    async function fetchTickets(boardId) {
        try {
            const data = await apiFetch(`/tickets/?board_id=${boardId}`)
            // 清除舊資料，保留非此 board 的 (或乾脆全清，視需求)
            const otherTickets = allTickets.value.filter(t => t.board_id !== Number(boardId))
            allTickets.value = [...otherTickets, ...data]
        } catch (error) {
            console.error('Fetch tickets failed:', error)
        }
    }

    async function createTicket(ticketData) {
        // ticketData: { boardId, columnId, title, description, priority, startDate, dueDate }
        // 轉成 API 需要的 snake_case
        const payload = {
            board_id: ticketData.boardId,
            column_id: ticketData.columnId,
            title: ticketData.title,
            description: ticketData.description,
            priority: ticketData.priority,
            start_date: ticketData.startDate || null,
            due_date: ticketData.dueDate || null
        }

        try {
            const newTicket = await apiFetch('/tickets/', {
                method: 'POST',
                body: JSON.stringify(payload)
            })
            allTickets.value.push(newTicket)
            return newTicket
        } catch (error) {
            console.error('Create ticket failed:', error)
            throw error
        }
    }

    async function updateTicket(ticketId, updates) {
        try {
            // updates key 可能需要轉換 (例如 columnId -> column_id)
            const payload = {}
            if (updates.title !== undefined) payload.title = updates.title
            if (updates.description !== undefined) payload.description = updates.description
            if (updates.priority !== undefined) payload.priority = updates.priority
            if (updates.columnId !== undefined) payload.column_id = updates.columnId
            if (updates.position !== undefined) payload.position = updates.position
            // 日期處理
            if (updates.startDate !== undefined) payload.start_date = updates.startDate
            if (updates.dueDate !== undefined) payload.due_date = updates.dueDate

            const updatedTicket = await apiFetch(`/tickets/${ticketId}`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            })

            // 更新本地 State
            const idx = allTickets.value.findIndex(t => t.id === ticketId)
            if (idx !== -1) {
                allTickets.value[idx] = updatedTicket
            }
        } catch (error) {
            console.error('Update ticket failed:', error)
        }
    }

    async function moveTicket(ticketId, newColumnId) {
        // 樂觀 UI 更新 (Optimistic Query)
        // 先改本地，再送 API。失敗再改回來? 
        // 這裡先簡單做：直接送 API 成功才改
        await updateTicket(ticketId, { columnId: newColumnId })
    }

    async function deleteTicket(ticketId) {
        try {
            await apiFetch(`/tickets/${ticketId}`, {
                method: 'DELETE'
            })
            // Remove from local state
            allTickets.value = allTickets.value.filter(t => t.id !== ticketId)
        } catch (error) {
            console.error('Delete ticket failed:', error)
            throw error
        }
    }

    // 當刪除看板時，前端也要清空相關的 ticket
    function deleteTicketsByBoard(boardId) {
        allTickets.value = allTickets.value.filter(t => t.board_id !== Number(boardId))
    }

    // Getters
    const getTicketsByColumn = (columnId) => {
        return allTickets.value
            .filter(t => t.column_id === Number(columnId))
            .sort((a, b) => a.position - b.position)
    }

    const getTicketsByBoard = (boardId) => {
        return allTickets.value.filter(t => t.board_id === Number(boardId))
    }

    return {
        allTickets,
        fetchTickets,
        createTicket,
        updateTicket,
        moveTicket,
        deleteTicket,
        deleteTicketsByBoard,
        getTicketsByColumn,
        getTicketsByBoard
    }
})
