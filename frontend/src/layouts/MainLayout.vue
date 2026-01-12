<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { useBoardStore } from '../stores/boardStore'

const boardStore = useBoardStore()

// Sidebar 展開/收合狀態 (用於調整 main content 的 margin)
const sidebarCollapsed = ref(false)

onMounted(() => {
  boardStore.fetchBoards()
})
</script>

<template>
  <div class="min-h-screen bg-slate-950">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <main
      :class="[
        'transition-all duration-300 min-h-screen',
        'ml-64'  // 固定 margin，Sidebar 寬度
      ]"
    >
      <div class="p-6">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 當 Sidebar 收合時調整 margin */
.sidebar-collapsed main {
  margin-left: 4rem; /* 64px */
}
</style>
