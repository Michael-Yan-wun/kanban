<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import draggable from 'vuedraggable'
import { useBoardStore } from '../stores/boardStore'
import { useColumnStore } from '../stores/columnStore'
import { useTicketStore } from '../stores/ticketStore'
import TicketModal from '../components/TicketModal.vue'
import Modal from '../components/Modal.vue'

const route = useRoute()
const router = useRouter()
const boardStore = useBoardStore()
const columnStore = useColumnStore()
const ticketStore = useTicketStore()
const isLoading = ref(false)
const isSubmitting = ref(false)

// 當前看板
const currentBoard = computed(() => boardStore.currentBoard)

// 當前看板的欄位
const columns = computed(() => {
  const boardId = parseInt(route.params.id)
  return columnStore.getColumnsByBoard(boardId)
})

// 每個欄位的票券 (用於 vuedraggable)
const columnTickets = ref({})

// 從 Store 分類票券 (同步動作)
function organizeTickets() {
  const result = {}
  columns.value.forEach(col => {
    result[col.id] = ticketStore.getTicketsByColumn(col.id)
  })
  columnTickets.value = result
}

// 載入資料 (非同步 API)
async function loadBoardData() {
  const boardId = parseInt(route.params.id)
  if (!boardId) return

  isLoading.value = true
  try {
      // 平行載入所有資料
      await Promise.all([
          boardStore.fetchBoardDetail(boardId),
          columnStore.fetchColumns(boardId),
          ticketStore.fetchTickets(boardId)
      ])
      // 資料載入完成後，整理票券
      organizeTickets()
  } catch (e) {
      console.error(e)
  } finally {
      isLoading.value = false
  }
}

// 顏色對應
const colorClasses = {
  slate: 'bg-slate-500',
  blue: 'bg-blue-500',
  green: 'bg-green-500',
  red: 'bg-red-500',
  yellow: 'bg-yellow-500',
  purple: 'bg-purple-500',
  pink: 'bg-pink-500',
  orange: 'bg-orange-500'
}

const colorOptions = [
  { value: 'slate', label: '灰色' },
  { value: 'blue', label: '藍色' },
  { value: 'green', label: '綠色' },
  { value: 'red', label: '紅色' },
  { value: 'yellow', label: '黃色' },
  { value: 'purple', label: '紫色' },
  { value: 'pink', label: '粉色' },
  { value: 'orange', label: '橙色' }
]

// ===== Ticket Modal =====
const showTicketModal = ref(false)
const isEditingTicket = ref(false)
const editingTicket = ref(null)
const currentColumnId = ref(null)

function openAddTicketModal(columnId) {
  isEditingTicket.value = false
  editingTicket.value = null
  currentColumnId.value = columnId
  showTicketModal.value = true
}

function openEditTicketModal(ticket) {
  isEditingTicket.value = true
  editingTicket.value = { ...ticket }
  currentColumnId.value = ticket.columnId
  showTicketModal.value = true
}

async function saveTicket(data) {
  const boardId = parseInt(route.params.id)
  isSubmitting.value = true
  
  try {
    if (isEditingTicket.value && editingTicket.value) {
      // 更新票券
      const updatedData = { ...data, columnId: data.columnId || currentColumnId.value }
      await ticketStore.updateTicket(editingTicket.value.id, updatedData)
    } else {
      // 新增票券
      await ticketStore.createTicket({
        ...data,
        boardId,
        columnId: currentColumnId.value
      })
    }
    organizeTickets()
    showTicketModal.value = false
  } catch (e) {
    console.error(e)
    alert('操作失敗，請重試')
  } finally {
    isSubmitting.value = false
  }
}

async function deleteTicket(ticketId) {
  if (!confirm('確定要刪除此任務嗎？')) return
  
  isSubmitting.value = true
  try {
    await ticketStore.deleteTicket(ticketId)
    organizeTickets()
    showTicketModal.value = false
  } catch(e) {
     console.error(e)
     alert('刪除失敗')
  } finally {
    isSubmitting.value = false
  }
}

// 拖曳結束時同步 columnId
function onDragEnd(columnId) {
  const tickets = columnTickets.value[columnId] || []
  tickets.forEach(ticket => {
    if (ticket.columnId !== columnId) {
      ticketStore.updateTicket(ticket.id, { columnId })
      ticket.columnId = columnId
    }
  })
}

// ===== Column Modal =====
const showColumnModal = ref(false)
const isEditingColumn = ref(false)
const editingColumn = ref(null)
const columnFormData = ref({ name: '', color: 'slate' })

// 刪除確認
const showDeleteConfirm = ref(false)
const deletingColumn = ref(null)

function openAddColumnModal() {
  isEditingColumn.value = false
  editingColumn.value = null
  columnFormData.value = { name: '', color: 'slate' }
  showColumnModal.value = true
}

function openEditColumnModal(column) {
  isEditingColumn.value = true
  editingColumn.value = column
  columnFormData.value = { name: column.name, color: column.color }
  showColumnModal.value = true
}

async function saveColumn() {
  if (!columnFormData.value.name.trim()) return

  const boardId = parseInt(route.params.id)
  isSubmitting.value = true

  try {
    if (isEditingColumn.value && editingColumn.value) {
      await columnStore.updateColumn(editingColumn.value.id, columnFormData.value)
    } else {
      await columnStore.createColumn({
        boardId,
        name: columnFormData.value.name,
        color: columnFormData.value.color
      })
    }
  
    organizeTickets()
    showColumnModal.value = false
  } catch (e) {
    console.error(e)
    alert('儲存失敗')
  } finally {
    isSubmitting.value = false
  }
}

function openDeleteColumnConfirm(column) {
  deletingColumn.value = column
  showDeleteConfirm.value = true
}

async function confirmDeleteColumn() {
  if (!deletingColumn.value) return

  isSubmitting.value = true
  try {
    // 刪除該欄位的所有票券 (這應該在後端做，但若後端無 cascade delete，這裡需要 loop)
    // 假設後端沒有自動刪除關聯，我們前端暫時先這樣做，雖然效率不好
    const tickets = ticketStore.getTicketsByColumn(deletingColumn.value.id)
    await Promise.all(tickets.map(t => ticketStore.deleteTicket(t.id)))

    // 刪除欄位
    await columnStore.deleteColumn(deletingColumn.value.id)
  
    organizeTickets()
    showDeleteConfirm.value = false
    deletingColumn.value = null
  } catch (e) {
     console.error(e)
     alert('刪除失敗')
  } finally {
     isSubmitting.value = false
  }
}

// 優先級相關
const priorityLabels = { low: '低', medium: '中', high: '高' }

function formatDate(utcString) {
  if (!utcString) return null
  const date = new Date(utcString)
  return date.toLocaleDateString('zh-TW', {
    timeZone: 'Asia/Taipei',
    month: 'short',
    day: 'numeric'
  })
}

// 監聽路由變化，重新載入
watch(() => route.params.id, (newId) => {
  if (newId) loadBoardData()
}, { immediate: true })

// 監聽 Store 中的票券變化 (例如新增/移動後)，自動重新整理
watch(() => ticketStore.allTickets, () => {
    organizeTickets()
}, { deep: true })
</script>

<template>
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
      <svg class="animate-spin h-10 w-10 text-blue-500 mb-4" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
      <p class="text-slate-400">載入看板資料中...</p>
    </div>
    <div v-else-if="currentBoard">

    <!-- Board Header -->
    <div class="mb-6">
      <div class="flex items-center gap-3 mb-2">
        <button
          @click="router.push('/boards')"
          class="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
          title="返回看板列表"
        >
          ←
        </button>
        <h1 class="text-2xl font-bold text-white">{{ currentBoard.name }}</h1>
      </div>
      <p class="text-slate-400 ml-11">{{ currentBoard.description }}</p>
    </div>

    <!-- Kanban Board -->
    <div class="flex gap-6 overflow-x-auto pb-4">
      <!-- Columns -->
      <div
        v-for="column in columns"
        :key="column.id"
        class="bg-slate-800/30 rounded-xl p-4 min-w-[300px] flex-shrink-0"
      >
        <!-- Column Header -->
        <div class="flex items-center justify-between mb-4 group">
          <div class="flex items-center gap-2">
            <div :class="['w-3 h-3 rounded-full', colorClasses[column.color] || 'bg-slate-500']"></div>
            <h2 class="font-semibold text-slate-200">{{ column.name }}</h2>
            <span class="bg-slate-700 text-slate-300 text-xs px-2 py-0.5 rounded-full">
              {{ (columnTickets[column.id] || []).length }}
            </span>
          </div>
          <div class="flex gap-1">
            <button
              @click="openEditColumnModal(column)"
              class="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-white transition-all"
              title="編輯欄位"
            >
              ✏️
            </button>
            <button
              @click="openDeleteColumnConfirm(column)"
              class="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition-all"
              title="刪除欄位"
            >
              🗑️
            </button>
            <button
              @click="openAddTicketModal(column.id)"
              class="p-1.5 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
              title="新增任務"
            >
              ➕
            </button>
          </div>
        </div>

        <!-- Draggable Tickets -->
        <draggable
          v-model="columnTickets[column.id]"
          group="tickets"
          item-key="id"
          class="space-y-3 min-h-[200px]"
          ghost-class="opacity-50"
          @end="onDragEnd(column.id)"
        >
          <template #item="{ element }">
            <div
              @click="openEditTicketModal(element)"
              class="bg-gradient-to-br from-slate-800/80 to-slate-800/40 rounded-xl p-5 border border-slate-600/30 hover:border-blue-500/60 hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-300 cursor-pointer group"
            >
              <!-- Header: Priority & Delete -->
              <div class="flex items-center justify-between mb-3">
                <span
                  :class="[
                    'text-xs px-2.5 py-1 rounded-lg font-medium',
                    element.priority === 'high' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                    element.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                    'bg-slate-600/50 text-slate-400 border border-slate-500/30'
                  ]"
                >
                  {{ priorityLabels[element.priority] }}優先
                </span>
                <button
                  @click.stop="deleteTicket(element.id)"
                  class="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-red-500/20 text-slate-500 hover:text-red-400 transition-all"
                  title="刪除"
                >
                  🗑️
                </button>
              </div>

              <!-- Title -->
              <h3 class="font-semibold text-white text-base mb-2 leading-snug">{{ element.title }}</h3>

              <!-- Description Preview -->
              <p v-if="element.description" class="text-sm text-slate-400 mb-3 line-clamp-2 leading-relaxed">
                {{ element.description }}
              </p>

              <!-- Footer: Date -->
              <div class="flex items-center justify-between pt-3 border-t border-slate-700/50">
                <div v-if="element.due_date" class="flex items-center gap-1.5 text-xs">
                  <span class="text-slate-500">📅</span>
                  <span class="text-slate-400">{{ formatDate(element.due_date) }}</span>
                </div>
                <div v-else class="text-xs text-slate-600">無截止日</div>
                <div class="flex items-center gap-1 text-xs text-slate-500">
                  <span>📝</span>
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>

      <!-- Add Column Button -->
      <div
        @click="openAddColumnModal"
        class="bg-slate-800/20 hover:bg-slate-800/40 border-2 border-dashed border-slate-700 hover:border-blue-500/50 rounded-xl p-4 min-w-[300px] flex-shrink-0 flex items-center justify-center cursor-pointer transition-all duration-200 group"
      >
        <div class="text-center">
          <div class="text-3xl mb-2 group-hover:scale-110 transition-transform">➕</div>
          <div class="text-slate-400 group-hover:text-white transition-colors">新增欄位</div>
        </div>
      </div>
    </div>

    <!-- Ticket Modal -->
    <TicketModal
      :show="showTicketModal"
      :isEditing="isEditingTicket"
      :ticket="editingTicket"
      :columnId="currentColumnId"
      @close="showTicketModal = false"
      @save="saveTicket"
      @delete="deleteTicket"
    />

    <!-- Column Modal -->
    <Modal
      :show="showColumnModal"
      @close="showColumnModal = false"
      :title="isEditingColumn ? '編輯欄位' : '新增欄位'"
    >
      <form @submit.prevent="saveColumn" class="space-y-4">
        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">欄位名稱</label>
          <input
            v-model="columnFormData.name"
            type="text"
            placeholder="例如：待辦事項"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Color -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">顏色</label>
          <div class="grid grid-cols-4 gap-2">
            <button
              v-for="opt in colorOptions"
              :key="opt.value"
              type="button"
              @click="columnFormData.color = opt.value"
              :class="[
                'flex items-center gap-2 px-3 py-2 rounded-lg border transition-all',
                columnFormData.color === opt.value
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-slate-600 hover:border-slate-500'
              ]"
            >
              <div :class="['w-3 h-3 rounded-full', colorClasses[opt.value]]"></div>
              <span class="text-sm text-slate-300">{{ opt.label }}</span>
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 pt-2">
          <button
            type="button"
            @click="showColumnModal = false"
            class="px-4 py-2 text-slate-300 hover:text-white transition-colors"
          >
            取消
          </button>
          <button
            type="submit"
            class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
          >
            {{ isEditingColumn ? '儲存' : '新增' }}
            <span v-if="isSubmitting" class="ml-2 animate-spin">⌛</span>
          </button>
        </div>
      </form>
    </Modal>

    <!-- Delete Column Confirm Modal -->
    <Modal
      :show="showDeleteConfirm"
      @close="showDeleteConfirm = false"
      title="確認刪除"
    >
      <div class="text-center py-4">
        <div class="text-5xl mb-4">⚠️</div>
        <p class="text-lg text-white mb-2">
          確定要刪除欄位「{{ deletingColumn?.name }}」嗎？
        </p>
        <p class="text-sm text-slate-400">
          該欄位內的所有任務也會一併刪除
        </p>
      </div>
      <div class="flex justify-center gap-3 pt-4">
        <button
          @click="showDeleteConfirm = false"
          class="px-5 py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
        >
          取消
        </button>
        <button
          @click="confirmDeleteColumn"
          :disabled="isSubmitting"
          class="px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors flex items-center disabled:opacity-50"
        >
          <span v-if="isSubmitting" class="mr-2 animate-spin">⌛</span>
          確認刪除
        </button>
      </div>
    </Modal>
  </div>

  <!-- Loading or Not Found -->
  <div v-else class="flex flex-col items-center justify-center py-16 text-slate-400">
    <span class="text-5xl mb-4">🔍</span>
    <p class="text-lg">找不到此看板</p>
    <button
      @click="router.push('/boards')"
      class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
    >
      返回看板列表
    </button>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
