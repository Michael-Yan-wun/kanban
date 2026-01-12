<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/userStore'
import { useAuthStore } from '../stores/authStore'
import Modal from '../components/Modal.vue'

const userStore = useUserStore()
const authStore = useAuthStore()
const isSubmitting = ref(false)

// 當前登入用戶
const currentUser = computed(() => authStore.currentUser)

// 用戶列表
const users = computed(() => userStore.allUsers)

// 初始化載入
onMounted(() => {
  userStore.fetchUsers()
})

// Modal 控制
const showModal = ref(false)
const isEditing = ref(false)
const editingUserId = ref(null)
const formData = ref({
  username: '',
  password: '',
  name: '',
  email: '',
  role: 'user'
})
const errorMsg = ref('')

// 刪除確認 Modal
const showDeleteConfirm = ref(false)
const deletingUser = ref(null)

// 開啟新增 Modal
function openAddModal() {
  isEditing.value = false
  editingUserId.value = null
  formData.value = {
    username: '',
    password: '',
    name: '',
    email: '',
    role: 'user'
  }
  errorMsg.value = ''
  showModal.value = true
}

// 開啟編輯 Modal
function openEditModal(user) {
  isEditing.value = true
  editingUserId.value = user.id
  formData.value = {
    username: user.username,
    password: '', // 不顯示密碼
    name: user.name,
    email: user.email || '',
    role: user.role
  }
  errorMsg.value = ''
  showModal.value = true
}

// 儲存用戶
async function saveUser() {
  errorMsg.value = ''
  isSubmitting.value = true

  try {
    if (isEditing.value) {
      // 更新用戶
      const updateData = {
        name: formData.value.name,
        email: formData.value.email,
        role: formData.value.role
      }
      
      if (formData.value.password) {
        updateData.password = formData.value.password
      }

      const result = await userStore.updateUser(editingUserId.value, updateData)
      if (!result.success) {
        errorMsg.value = result.message
        return
      }
    } else {
      // 新增用戶
      if (!formData.value.username || !formData.value.password || !formData.value.name) {
        errorMsg.value = '請填寫所有必填欄位'
        return
      }

      const result = await userStore.createUser(formData.value)
      if (!result.success) {
        errorMsg.value = result.message
        return
      }
    }
    showModal.value = false
  } catch (error) {
    errorMsg.value = '發生錯誤'
  } finally {
    isSubmitting.value = false
  }
}

// 開啟刪除確認 Modal
function openDeleteConfirm(userId) {
  // 檢查權限
  if (!canDelete(userId)) {
    return
  }

  const user = userStore.getUserById(userId)
  if (!user) return

  deletingUser.value = user
  showDeleteConfirm.value = true
}

// 確認刪除
async function confirmDelete() {
  if (!deletingUser.value) return
  isSubmitting.value = true

  const result = await userStore.deleteUser(deletingUser.value.id)
  if (!result.success) {
    alert(result.message)
  }

  showDeleteConfirm.value = false
  deletingUser.value = null
  isSubmitting.value = false
}

// 取消刪除
function cancelDelete() {
  showDeleteConfirm.value = false
  deletingUser.value = null
}

// 判斷是否可以刪除某用戶
function canDelete(userId) {
  // 只有 admin 可以刪除
  if (!authStore.isAdmin) return false
  // 不能刪除自己
  if (currentUser.value?.id === userId) return false
  return true
}

// 已移除重設密碼功能，密碼可在編輯時更改

// 格式化日期
function formatDate(utcString) {
  if (!utcString) return '-'
  return new Date(utcString).toLocaleDateString('zh-TW', {
    timeZone: 'Asia/Taipei',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-white">👥 用戶管理</h1>
        <p class="text-slate-400 mt-1">管理系統用戶帳號</p>
      </div>
      <button
        @click="openAddModal"
        class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2 transition-colors font-medium"
      >
        <span>➕</span>
        <span>新增用戶</span>
      </button>
    </div>

    <!-- Users Table -->
    <div class="bg-slate-800/50 rounded-xl border border-slate-700/50 overflow-hidden">
      <table class="w-full">
        <thead class="bg-slate-800">
          <tr>
            <th class="px-6 py-4 text-left text-sm font-medium text-slate-300">用戶名稱</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-slate-300">姓名</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-slate-300">Email</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-slate-300">角色</th>
            <th class="px-6 py-4 text-left text-sm font-medium text-slate-300">建立日期</th>
            <th class="px-6 py-4 text-right text-sm font-medium text-slate-300">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-700/50">
          <tr v-for="user in users" :key="user.id" class="hover:bg-slate-800/30 transition-colors">
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-medium">
                  {{ user.name?.charAt(0) || '?' }}
                </div>
                <span class="text-white font-medium">{{ user.username }}</span>
              </div>
            </td>
            <td class="px-6 py-4 text-slate-300">{{ user.name }}</td>
            <td class="px-6 py-4 text-slate-400">{{ user.email || '-' }}</td>
            <td class="px-6 py-4">
              <span
                :class="[
                  'px-2.5 py-1 rounded-full text-xs font-medium',
                  user.role === 'admin' ? 'bg-purple-500/20 text-purple-400' : 'bg-slate-600/50 text-slate-300'
                ]"
              >
                {{ user.role === 'admin' ? '管理員' : '成員' }}
              </span>
            </td>
            <td class="px-6 py-4 text-slate-400 text-sm">{{ formatDate(user.createdAt) }}</td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-end gap-1">
                <button
                  @click="openEditModal(user)"
                  class="px-3 py-1.5 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-white transition-colors text-sm"
                  title="編輯"
                >
                  ✏️ 編輯
                </button>
                <button
                  v-if="canDelete(user.id)"
                  @click.stop="openDeleteConfirm(user.id)"
                  class="px-3 py-1.5 rounded-lg hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition-colors text-sm"
                  title="刪除"
                >
                  🗑️ 刪除
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="users.length === 0" class="text-center py-12 text-slate-400">
        暫無用戶資料
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <Modal
      :show="showModal"
      @close="showModal = false"
      :title="isEditing ? '編輯用戶' : '新增用戶'"
    >
      <form @submit.prevent="saveUser" class="space-y-4">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">
            用戶名稱 <span class="text-red-400">*</span>
          </label>
          <input
            v-model="formData.username"
            type="text"
            :disabled="isEditing"
            placeholder="登入用的帳號"
            :class="[
              'w-full px-3 py-2.5 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500',
              isEditing ? 'bg-slate-600 cursor-not-allowed' : 'bg-slate-700'
            ]"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">
            密碼 
            <span v-if="!isEditing" class="text-red-400">*</span>
            <span v-else class="text-slate-500 text-xs">(留空則不更改)</span>
          </label>
          <input
            v-model="formData.password"
            type="password"
            :placeholder="isEditing ? '輸入新密碼' : '設定密碼'"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">
            姓名 <span class="text-red-400">*</span>
          </label>
          <input
            v-model="formData.name"
            type="text"
            placeholder="顯示名稱"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">Email</label>
          <input
            v-model="formData.email"
            type="email"
            placeholder="user@example.com"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Role -->
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1.5">角色</label>
          <select
            v-model="formData.role"
            class="w-full px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="user">成員</option>
            <option value="admin">管理員</option>
          </select>
        </div>

        <!-- Error Message -->
        <div v-if="errorMsg" class="text-red-400 text-sm text-center py-2 bg-red-500/10 rounded-lg">
          {{ errorMsg }}
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
          </button>
        </div>
      </form>
    </Modal>

    <!-- 刪除確認 Modal -->
    <Modal
      :show="showDeleteConfirm"
      @close="cancelDelete"
      title="確認刪除"
    >
      <div class="text-center py-4">
        <div class="text-5xl mb-4">⚠️</div>
        <p class="text-lg text-white mb-2">
          確定要刪除用戶「{{ deletingUser?.name }}」嗎？
        </p>
        <p class="text-sm text-slate-400">
          此操作無法復原
        </p>
      </div>
      <div class="flex justify-center gap-3 pt-4">
        <button
          @click="cancelDelete"
          class="px-5 py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
        >
          取消
        </button>
        <button
          @click="confirmDelete"
          class="px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
        >
          確認刪除
        </button>
      </div>
    </Modal>
  </div>
</template>
