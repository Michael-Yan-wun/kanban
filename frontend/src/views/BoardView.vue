<script setup>
import { ref, computed } from 'vue'
import draggable from 'vuedraggable'
import Modal from '../components/Modal.vue'

// ===== 三個獨立的資料陣列 =====
const newList = ref([
  { id: 1, title: '統計報表頁面', description: '視覺化數據呈現', priority: 'medium' },
  { id: 2, title: '優化使用者體驗', description: '動畫效果與響應式設計', priority: 'low' }
])

const inProgressList = ref([
  { id: 3, title: '實作看板功能', description: '拖放功能與狀態管理', priority: 'high' }
])

const doneList = ref([
  { id: 4, title: '建立專案架構', description: '設定 Vue 3 + Vite 開發環境', priority: 'high' },
  { id: 5, title: '設計登入頁面', description: '包含表單驗證功能', priority: 'medium' }
])

// ===== 欄位定義 =====
const columns = computed(() => [
  { id: 'new', title: '待辦事項', color: 'bg-slate-500', list: newList },
  { id: 'inProgress', title: '進行中', color: 'bg-blue-500', list: inProgressList },
  { id: 'done', title: '已完成', color: 'bg-green-500', list: doneList }
])

// ===== Modal 控制 =====
const showModal = ref(false)
const isEditing = ref(false)
const editingTicketId = ref(null)

const formData = ref({
  title: '',
  description: '',
  priority: 'medium'
})

// ===== 優先級設定 =====
const priorityOptions = [
  { value: 'low', label: '低', color: 'bg-slate-500' },
  { value: 'medium', label: '中', color: 'bg-yellow-500' },
  { value: 'high', label: '高', color: 'bg-red-500' }
]

function getPriorityColor(priority) {
  return priorityOptions.find(p => p.value === priority)?.color || 'bg-slate-500'
}

function getPriorityLabel(priority) {
  return priorityOptions.find(p => p.value === priority)?.label || '中'
}

// ===== 開啟新增 Modal =====
function openAddModal() {
  isEditing.value = false
  editingTicketId.value = null
  formData.value = { title: '', description: '', priority: 'medium' }
  showModal.value = true
}

// ===== 開啟編輯 Modal =====
function openEditModal(ticket) {
  isEditing.value = true
  editingTicketId.value = ticket.id
  formData.value = {
    title: ticket.title,
    description: ticket.description,
    priority: ticket.priority
  }
  showModal.value = true
}

// ===== 儲存票券 (新增/編輯) =====
function saveTicket() {
  if (!formData.value.title.trim()) return

  if (isEditing.value) {
    // 編輯模式：遍歷三個陣列找到對應 ID 並更新
    const lists = [newList, inProgressList, doneList]
    for (const list of lists) {
      const idx = list.value.findIndex(t => t.id === editingTicketId.value)
      if (idx !== -1) {
        list.value[idx] = {
          ...list.value[idx],
          title: formData.value.title,
          description: formData.value.description,
          priority: formData.value.priority
        }
        break
      }
    }
  } else {
    // 新增模式：加入 newList
    newList.value.push({
      id: Date.now(),
      title: formData.value.title,
      description: formData.value.description,
      priority: formData.value.priority
    })
  }

  showModal.value = false
}

// ===== 刪除票券 =====
function deleteTicket(ticketId) {
  const lists = [newList, inProgressList, doneList]
  for (const list of lists) {
    const idx = list.value.findIndex(t => t.id === ticketId)
    if (idx !== -1) {
      list.value.splice(idx, 1)
      break
    }
  }
}

// ===== 暴露給 StatsView 使用 (透過 provide) =====
import { provide } from 'vue'
provide('kanbanData', { newList, inProgressList, doneList })
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-white">📋 我的看板</h1>
      <button
        @click="openAddModal"
        class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg flex items-center gap-2 transition-colors"
      >
        <span>➕</span>
        <span>新增任務</span>
      </button>
    </div>

    <!-- Kanban Board -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div
        v-for="column in columns"
        :key="column.id"
        class="bg-slate-800/50 rounded-xl p-4 min-h-[500px]"
      >
        <!-- Column Header -->
        <div class="flex items-center gap-2 mb-4">
          <div :class="['w-3 h-3 rounded-full', column.color]"></div>
          <h2 class="font-semibold text-slate-200">{{ column.title }}</h2>
          <span class="ml-auto bg-slate-700 text-slate-300 text-xs px-2 py-1 rounded-full">
            {{ column.list.length }}
          </span>
        </div>

        <!-- Draggable Tickets -->
        <draggable
          v-model="column.list.value"
          group="tickets"
          item-key="id"
          class="space-y-3 min-h-[100px]"
          ghost-class="opacity-50"
          drag-class="rotate-2"
        >
          <template #item="{ element }">
            <div
              @click="openEditModal(element)"
              class="bg-slate-700/50 rounded-lg p-4 border border-slate-600/50 hover:border-indigo-500/50 transition-all duration-200 cursor-pointer group"
            >
              <!-- Priority Badge & Delete -->
              <div class="flex items-center justify-between mb-2">
                <span
                  :class="['text-xs px-2 py-0.5 rounded-full text-white', getPriorityColor(element.priority)]"
                >
                  {{ getPriorityLabel(element.priority) }}
                </span>
                <button
                  @click.stop="deleteTicket(element.id)"
                  class="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-red-400 transition-all"
                  title="刪除"
                >
                  🗑️
                </button>
              </div>

              <!-- Title -->
              <h3 class="font-medium text-white mb-1">{{ element.title }}</h3>

              <!-- Description (truncated) -->
              <p class="text-sm text-slate-400 line-clamp-2">{{ element.description }}</p>
            </div>
          </template>
        </draggable>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <Modal
      :show="showModal"
      @close="showModal = false"
      :title="isEditing ? '編輯任務' : '新增任務'"
    >
      <form @submit.prevent="saveTicket" class="space-y-4">
        <!-- Title -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1">標題</label>
          <input
            v-model="formData.title"
            type="text"
            placeholder="輸入任務標題"
            class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1">描述</label>
          <textarea
            v-model="formData.description"
            placeholder="輸入任務描述"
            rows="3"
            class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
          ></textarea>
        </div>

        <!-- Priority -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1">優先級</label>
          <select
            v-model="formData.priority"
            class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option v-for="opt in priorityOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
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
            class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg transition-colors"
          >
            {{ isEditing ? '儲存' : '新增' }}
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

/* 拖曳時的旋轉效果 */
.rotate-2 {
  transform: rotate(2deg);
}
</style>
