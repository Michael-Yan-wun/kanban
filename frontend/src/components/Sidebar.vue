<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { useBoardStore } from '../stores/boardStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const boardStore = useBoardStore()

// 側邊欄展開/收合狀態
const isCollapsed = ref(false)

// 用戶可見的看板列表
const boards = computed(() => boardStore.allBoards)

// 目前選中的看板 ID
const currentBoardId = computed(() => {
  const id = route.params.id
  return id ? parseInt(id) : null
})

// 導航項目
const navItems = computed(() => {
  const items = [
    { 
      id: 'boards', 
      name: '看板列表', 
      icon: '📋', 
      path: '/boards',
      active: route.path === '/boards'
    }
  ]

  // Admin 專屬功能
  if (authStore.isAdmin) {
    items.push(
      { id: 'divider-admin', type: 'divider', label: '管理功能' },
      { 
        id: 'admin-dashboard', 
        name: '全站統計', 
        icon: '📊', 
        path: '/admin/dashboard',
        active: route.path === '/admin/dashboard'
      },
      { 
        id: 'admin-users', 
        name: '用戶管理', 
        icon: '👥', 
        path: '/admin/users',
        active: route.path === '/admin/users'
      }
    )
  }

  return items
})

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

function navigateTo(path) {
  router.push(path)
}

function navigateToBoard(boardId) {
  router.push(`/boards/${boardId}`)
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <aside
    :class="[
      'fixed left-0 top-0 h-full bg-slate-900 border-r border-slate-700/50 transition-all duration-300 z-40 flex flex-col',
      isCollapsed ? 'w-16' : 'w-64'
    ]"
  >
    <!-- Logo & Toggle -->
    <div class="flex items-center justify-between p-4 border-b border-slate-700/50">
      <div v-if="!isCollapsed" class="flex items-center gap-2">
        <span class="text-xl">🎯</span>
        <span class="font-bold text-lg text-white">Kanban</span>
      </div>
      <button
        @click="toggleSidebar"
        class="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
        :title="isCollapsed ? '展開選單' : '收合選單'"
      >
        <span v-if="isCollapsed">▶</span>
        <span v-else>◀</span>
      </button>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto py-4">
      <!-- Main Nav Items -->
      <div class="px-3 space-y-1">
        <template v-for="item in navItems" :key="item.id">
          <!-- Divider -->
          <div v-if="item.type === 'divider'" class="pt-4 pb-2">
            <div v-if="!isCollapsed" class="text-xs font-medium text-slate-500 uppercase tracking-wider px-3">
              {{ item.label }}
            </div>
            <div v-else class="border-t border-slate-700 mx-2"></div>
          </div>
          
          <!-- Nav Link -->
          <button
            v-else
            @click="navigateTo(item.path)"
            :class="[
              'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200',
              item.active 
                ? 'bg-blue-600/20 text-blue-400' 
                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
            ]"
            :title="isCollapsed ? item.name : ''"
          >
            <span class="text-lg">{{ item.icon }}</span>
            <span v-if="!isCollapsed" class="font-medium">{{ item.name }}</span>
          </button>
        </template>
      </div>

      <!-- Boards List -->
      <div class="mt-6 px-3">
        <div v-if="!isCollapsed" class="flex items-center justify-between px-3 mb-2">
          <span class="text-xs font-medium text-slate-500 uppercase tracking-wider">我的看板</span>
          <span class="text-xs text-slate-500">{{ boards.length }}</span>
        </div>
        <div v-else class="border-t border-slate-700 mx-2 mb-3"></div>

        <div class="space-y-1">
          <button
            v-for="board in boards"
            :key="board.id"
            @click="navigateToBoard(board.id)"
            :class="[
              'w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200',
              currentBoardId === board.id
                ? 'bg-blue-600/20 text-blue-400'
                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
            ]"
            :title="isCollapsed ? board.name : ''"
          >
            <span class="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0"></span>
            <span v-if="!isCollapsed" class="truncate text-sm">{{ board.name }}</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- User & Logout -->
    <div class="border-t border-slate-700/50 p-4">
      <div v-if="!isCollapsed" class="flex items-center gap-3 mb-3">
        <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-medium">
          {{ authStore.currentUser?.name?.charAt(0) || '?' }}
        </div>
        <div class="flex-1 min-w-0">
          <div class="text-sm font-medium text-white truncate">{{ authStore.currentUser?.name }}</div>
          <div class="text-xs text-slate-400">{{ authStore.isAdmin ? '管理員' : '成員' }}</div>
        </div>
      </div>
      
      <button
        @click="logout"
        :class="[
          'w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:bg-red-500/20 hover:text-red-400 transition-colors',
          isCollapsed ? 'justify-center' : ''
        ]"
        :title="isCollapsed ? '登出' : ''"
      >
        <span>🚪</span>
        <span v-if="!isCollapsed">登出</span>
      </button>
    </div>
  </aside>
</template>
