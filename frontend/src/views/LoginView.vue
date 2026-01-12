<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  errorMsg.value = ''

  if (!username.value.trim() || !password.value.trim()) {
    errorMsg.value = '請輸入帳號和密碼'
    return
  }

  isLoading.value = true

  // 模擬 API 延遲
  await new Promise(resolve => setTimeout(resolve, 600))

  const result = await authStore.login(username.value, password.value)

  if (result.success) {
    router.push('/boards')
  } else {
    errorMsg.value = result.message || '登入失敗'
  }

  isLoading.value = false
}
</script>

<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Login Card -->
      <div class="bg-slate-900/80 backdrop-blur-xl rounded-2xl p-8 border border-slate-800 shadow-2xl">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="text-5xl mb-4">🎯</div>
          <h1 class="text-2xl font-bold text-white mb-2">Kanban 看板系統</h1>
          <p class="text-slate-400">登入以繼續使用</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Username -->
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-2">帳號</label>
            <input
              v-model="username"
              type="text"
              placeholder="請輸入帳號"
              class="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-2">密碼</label>
            <input
              v-model="password"
              type="password"
              placeholder="請輸入密碼"
              class="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
          </div>

          <!-- Error Message -->
          <div v-if="errorMsg" class="text-red-400 text-sm text-center py-2 bg-red-500/10 rounded-lg border border-red-500/20">
            {{ errorMsg }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              登入中...
            </span>
            <span v-else>登入</span>
          </button>
        </form>

        <!-- Demo Hint -->
        <div class="mt-6 p-4 bg-slate-800/50 rounded-xl border border-slate-700/50">
          <p class="text-sm text-slate-400 mb-2">測試帳號：</p>
          <div class="space-y-1 text-sm">
            <p class="text-slate-300">
              <span class="text-purple-400 font-medium">管理員</span>：admin / admin123
            </p>
            <p class="text-slate-300">
              <span class="text-blue-400 font-medium">一般用戶</span>：user1 / user123
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
