<script setup>
import { ref, computed, watch } from 'vue'
import Modal from './Modal.vue'

const props = defineProps({
  show: { type: Boolean, default: false },
  isEditing: { type: Boolean, default: false },
  ticket: { type: Object, default: null },
  columnId: { type: Number, default: null }
})

const emit = defineEmits(['close', 'save', 'delete'])

// 表單資料
const formData = ref({
  title: '',
  description: '',
  priority: 'medium',
  startTime: '',
  endTime: ''
})

// 優先級選項
const priorityOptions = [
  { value: 'low', label: '低', color: 'bg-slate-500' },
  { value: 'medium', label: '中', color: 'bg-yellow-500' },
  { value: 'high', label: '高', color: 'bg-red-500' }
]

// UTC 轉本地時間 (UTC+8) 用於顯示
function utcToLocal(utcString) {
  if (!utcString) return ''
  const date = new Date(utcString)
  // 轉換為 datetime-local 格式
  const offset = 8 * 60 // UTC+8
  const localDate = new Date(date.getTime() + offset * 60 * 1000)
  return localDate.toISOString().slice(0, 16)
}

// 本地時間轉 UTC 用於儲存
function localToUtc(localString) {
  if (!localString) return null
  // 假設輸入為 UTC+8
  const date = new Date(localString)
  // 減去 8 小時得到 UTC
  const utcDate = new Date(date.getTime() - 8 * 60 * 60 * 1000)
  return utcDate.toISOString()
}

// 格式化顯示時間 (UTC+8)
function formatDateTime(utcString) {
  if (!utcString) return '-'
  const date = new Date(utcString)
  return date.toLocaleString('zh-TW', {
    timeZone: 'Asia/Taipei',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 監聽 ticket 變化，填入表單
watch(() => props.ticket, (newTicket) => {
  if (newTicket) {
    // 相容後端回傳的 snake_case 或前端慣用的 camelCase
    const start = newTicket.start_date || newTicket.startDate
    const end = newTicket.due_date || newTicket.dueDate || newTicket.endTime

    formData.value = {
      title: newTicket.title || '',
      description: newTicket.description || '',
      priority: newTicket.priority || 'medium',
      startTime: utcToLocal(start),
      endTime: utcToLocal(end)
    }
  } else {
    formData.value = {
      title: '',
      description: '',
      priority: 'medium',
      startTime: '',
      endTime: ''
    }
  }
}, { immediate: true })

// 儲存
function handleSave() {
  if (!formData.value.title.trim()) return

  const data = {
    title: formData.value.title.trim(),
    description: formData.value.description.trim(),
    priority: formData.value.priority,
    // 統一使用 startDate / dueDate
    startDate: localToUtc(formData.value.startTime),
    dueDate: localToUtc(formData.value.endTime),
    columnId: props.columnId
  }

  emit('save', data)
}

// 刪除
function handleDelete() {
  if (props.ticket?.id) {
    emit('delete', props.ticket.id)
  }
}
</script>

<template>
  <Modal
    :show="show"
    @close="emit('close')"
    :title="isEditing ? '編輯任務' : '新增任務'"
  >
    <form @submit.prevent="handleSave" class="space-y-5">
      <!-- Title -->
      <div>
        <label class="block text-sm font-medium text-slate-300 mb-1.5">
          標題 <span class="text-red-400">*</span>
        </label>
        <input
          v-model="formData.title"
          type="text"
          placeholder="輸入任務標題"
          class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Description -->
      <div>
        <label class="block text-sm font-medium text-slate-300 mb-1.5">描述</label>
        <textarea
          v-model="formData.description"
          placeholder="輸入任務詳細描述..."
          rows="4"
          class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        ></textarea>
      </div>

      <!-- Priority -->
      <div>
        <label class="block text-sm font-medium text-slate-300 mb-1.5">優先級</label>
        <div class="flex gap-3">
          <label
            v-for="opt in priorityOptions"
            :key="opt.value"
            :class="[
              'flex-1 flex items-center justify-center gap-2 px-3 py-2.5 rounded-lg border cursor-pointer transition-all',
              formData.priority === opt.value
                ? 'border-blue-500 bg-blue-500/10 text-white'
                : 'border-slate-600 text-slate-400 hover:border-slate-500'
            ]"
          >
            <input
              type="radio"
              v-model="formData.priority"
              :value="opt.value"
              class="hidden"
            />
            <span :class="['w-2 h-2 rounded-full', opt.color]"></span>
            <span>{{ opt.label }}</span>
          </label>
        </div>
      </div>

      <!-- Time Range -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">開始時間</label>
          <input
            v-model="formData.startTime"
            type="datetime-local"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">結束時間</label>
          <input
            v-model="formData.endTime"
            type="datetime-local"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <!-- Meta Info (Edit mode) -->
      <div v-if="isEditing && ticket" class="pt-3 border-t border-slate-700">
        <p class="text-xs text-slate-500">
          建立於：{{ formatDateTime(ticket.createdAt) }} (UTC+8)
        </p>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-between pt-3">
        <button
          v-if="isEditing"
          type="button"
          @click="handleDelete"
          class="px-4 py-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors"
        >
          刪除任務
        </button>
        <div v-else></div>

        <div class="flex gap-3">
          <button
            type="button"
            @click="emit('close')"
            class="px-4 py-2 text-slate-300 hover:text-white transition-colors"
          >
            取消
          </button>
          <button
            type="submit"
            class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
          >
            {{ isEditing ? '儲存' : '新增' }}
          </button>
        </div>
      </div>
    </form>
  </Modal>
</template>
