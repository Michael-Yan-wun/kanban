<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isLoggedIn = computed(() => !!localStorage.getItem('kanban_user'))
const username = computed(() => {
  const user = localStorage.getItem('kanban_user')
  return user ? JSON.parse(user).name : ''
})

const navItems = [
  { name: '看板', path: '/board', icon: '📋' },
  { name: '統計', path: '/stats', icon: '📊' }
]

function logout() {
  localStorage.removeItem('kanban_user')
  router.push('/login')
}
</script>

<template>
  <nav class="bg-slate-800/80 backdrop-blur-md border-b border-slate-700 sticky top-0 z-50">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <span class="text-2xl">🎯</span>
          <span class="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            Kanban App
          </span>
        </div>

        <!-- Navigation Links -->
        <div v-if="isLoggedIn" class="flex items-center gap-6">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-700/50 transition-all duration-200"
            :class="{ 'bg-indigo-500/20 text-indigo-300': route.path === item.path }"
          >
            <span>{{ item.icon }}</span>
            <span>{{ item.name }}</span>
          </router-link>
        </div>

        <!-- User Menu -->
        <div v-if="isLoggedIn" class="flex items-center gap-4">
          <span class="text-slate-400 text-sm">👤 {{ username }}</span>
          <button
            @click="logout"
            class="px-4 py-2 text-sm bg-slate-700 hover:bg-red-500/80 rounded-lg transition-colors duration-200"
          >
            登出
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>
