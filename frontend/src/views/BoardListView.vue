<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBoardStore } from '../stores/boardStore'
import { useTicketStore } from '../stores/ticketStore'
import Modal from '../components/Modal.vue'

const router = useRouter()
const boardStore = useBoardStore()
const ticketStore = useTicketStore()

const isLoading = ref(false)
const isSubmitting = ref(false)

// 看板列表
const boards = computed(() => boardStore.allBoards)

onMounted(async () => {
  isLoading.value = true
  try {
    await boardStore.fetchBoards()
  } finally {
    isLoading.value = false
  }
})

// Modal 控制
const showModal = ref(false)
const isEditing = ref(false)
const editingBoardId = ref(null)
const formData = ref({
  name: '',
  description: ''
})

// 計算每個看板的統計
function getBoardStats(boardId) {
  const tickets = ticketStore.getTicketsByBoard(boardId)
  const total = tickets.length
  const done = tickets.filter(t => t.status === 'done').length
  const progress = total > 0 ? Math.round((done / total) * 100) : 0
  return { total, done, progress }
}

// 開啟新增 Modal
function openAddModal() {
  isEditing.value = false
  editingBoardId.value = null
  formData.value = { name: '', description: '' }
  showModal.value = true
}

// 開啟編輯 Modal
function openEditModal(board, event) {
  event.stopPropagation()
  isEditing.value = true
  editingBoardId.value = board.id
  formData.value = {
    name: board.name,
    description: board.description
  }
  showModal.value = true
}

// 儲存看板
async function saveBoard() {
  if (!formData.value.name.trim()) return

  isSubmitting.value = true
  try {
    if (isEditing.value) {
      await boardStore.updateBoard(editingBoardId.value, formData.value)
    } else {
      await boardStore.createBoard(formData.value)
    }
  
    showModal.value = false
  } catch (e) {
    console.error(e)
    alert('儲存失敗')
  } finally {
    isSubmitting.value = false
  }
}

// 刪除看板
async function deleteBoard(boardId, event) {
  event.stopPropagation()
  if (!confirm('確定要刪除此看板嗎？所有任務也會一併刪除。')) return

  try {
    // 這裡如果不加 isSubmitting 對 UI 影響不大，因為在列表頁直接刪除
    // 但為了保險起見，可以加個全域 loading 或局部 loading
    // 這裡從簡，直接 await
    await ticketStore.deleteTicketsByBoard(boardId)
    await boardStore.deleteBoard(boardId)
  } catch (e) {
    console.error(e)
    alert('刪除失敗')
  }
}

// 進入看板
function enterBoard(boardId) {
  router.push(`/boards/${boardId}`)
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-white">📋 我的看板</h1>
        <p class="text-slate-400 mt-1">管理您的專案與任務</p>
      </div>
      <button
        @click="openAddModal"
        class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2 transition-colors font-medium"
      >
        <span>➕</span>
        <span>新增看板</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
      <svg class="animate-spin h-10 w-10 text-blue-500 mb-4" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
      <p class="text-slate-400">載入看板中...</p>
    </div>

    <!-- Boards Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="board in boards"
        :key="board.id"
        @click="enterBoard(board.id)"
        class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50 hover:border-blue-500/50 transition-all duration-200 cursor-pointer group"
      >
        <!-- Board Header -->
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-white truncate">{{ board.name }}</h3>
            <p class="text-sm text-slate-400 mt-1 line-clamp-2">{{ board.description }}</p>
          </div>
          
          <!-- Actions -->
          <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              @click="openEditModal(board, $event)"
              class="p-2 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-white"
              title="編輯"
            >
              ✏️
            </button>
            <button
              @click="deleteBoard(board.id, $event)"
              class="p-2 rounded-lg hover:bg-red-500/20 text-slate-400 hover:text-red-400"
              title="刪除"
            >
              🗑️
            </button>
          </div>
        </div>

        <!-- Stats -->
        <div class="space-y-3">
          <div class="flex items-center justify-between text-sm">
            <span class="text-slate-400">任務進度</span>
            <span class="text-white font-medium">{{ getBoardStats(board.id).done }}/{{ getBoardStats(board.id).total }}</span>
          </div>
          
          <!-- Progress Bar -->
          <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-blue-500 to-blue-400 rounded-full transition-all duration-300"
              :style="{ width: `${getBoardStats(board.id).progress}%` }"
            ></div>
          </div>

          <div class="flex items-center justify-between text-xs text-slate-500">
            <span>{{ getBoardStats(board.id).progress }}% 完成</span>
            <span>👥 {{ board.members?.length || 1 }} 成員</span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-if="boards.length === 0"
        class="col-span-full flex flex-col items-center justify-center py-16 text-slate-400"
      >
        <span class="text-5xl mb-4">📭</span>
        <p class="text-lg mb-2">尚無看板</p>
        <p class="text-sm">點擊「新增看板」開始建立您的第一個專案</p>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <Modal
      :show="showModal"
      @close="showModal = false"
      :title="isEditing ? '編輯看板' : '新增看板'"
    >
      <form @submit.prevent="saveBoard" class="space-y-4">
        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1">看板名稱</label>
          <input
            v-model="formData.name"
            type="text"
            placeholder="例如：產品開發"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1">描述</label>
          <textarea
            v-model="formData.description"
            placeholder="簡述此看板的用途..."
            rows="3"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          ></textarea>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 pt-2">
          <button
            type="button"
            @click="showModal = false"
            class="px-4 py-2 text-slate-300 hover:text-white transition-colors"
          >
            取消
          </button>
          <button
            type="submit"
            class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
          >
            {{ isEditing ? '儲存' : '新增' }}
            <span v-if="isSubmitting" class="ml-2 animate-spin">⌛</span>
          </button>
        </div>
      </form>
    </Modal>
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
