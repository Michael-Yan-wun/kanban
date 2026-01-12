<script setup>
import { computed, ref, onMounted } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement
} from 'chart.js'
import { useBoardStore } from '../stores/boardStore'
import { useTicketStore } from '../stores/ticketStore'
import { useUserStore } from '../stores/userStore'
import { useColumnStore } from '../stores/columnStore'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, BarElement)

const boardStore = useBoardStore()
const ticketStore = useTicketStore()
const userStore = useUserStore()
const columnStore = useColumnStore()
const isLoading = ref(false)

onMounted(async () => {
  isLoading.value = true
  try {
    // 確保看板載入
    await boardStore.fetchBoards()
    // 平行載入所有看板的詳細資料 (票券、欄位) 以供統計
    const promises = boardStore.allBoards.map(board => Promise.all([
      ticketStore.fetchTickets(board.id),
      columnStore.fetchColumns(board.id)
    ]))
    await Promise.all(promises)
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

// 統計數據
const stats = computed(() => {
  const allTickets = ticketStore.allTickets
  const allColumns = columnStore.columns
  
  // 找出「完成」狀態的任務 (各看板中 position 最高的欄位)
  let doneCount = 0
  const doneColumnIds = new Set()
  
  boardStore.allBoards.forEach(board => {
    const boardCols = allColumns.filter(c => c.boardId === board.id)
    if (boardCols.length > 0) {
      const maxPos = Math.max(...boardCols.map(c => c.position))
      const doneCol = boardCols.find(c => c.position === maxPos)
      if (doneCol) doneColumnIds.add(doneCol.id)
    }
  })

  doneCount = allTickets.filter(t => doneColumnIds.has(t.column_id)).length

  return {
    totalBoards: boardStore.allBoards.length,
    totalTickets: allTickets.length,
    totalUsers: userStore.userCount,
    doneCount,
    highPriority: allTickets.filter(t => t.priority === 'high').length,
    mediumPriority: allTickets.filter(t => t.priority === 'medium').length,
    lowPriority: allTickets.filter(t => t.priority === 'low').length
  }
})

// 完成率
const completionRate = computed(() => {
  if (stats.value.totalTickets === 0) return 0
  return Math.round((stats.value.doneCount / stats.value.totalTickets) * 100)
})

// 各看板統計
const boardStats = computed(() => {
  return boardStore.allBoards.map(board => {
    const tickets = ticketStore.getTicketsByBoard(board.id)
    const columns = columnStore.getColumnsByBoard(board.id)
    
    // 定義最後一個欄位為「已完成」
    const doneColumn = columns.length > 0 ? columns[columns.length - 1] : null
    
    const total = tickets.length
    const done = doneColumn ? tickets.filter(t => t.column_id === doneColumn.id).length : 0
    const progress = total > 0 ? Math.round((done / total) * 100) : 0
    return { ...board, total, done, progress }
  })
})

// 狀態分佈圖的對應 (依名稱彙整)
const statusChartData = computed(() => {
  const allTickets = ticketStore.allTickets
  const allColumns = columnStore.columns
  
  const counts = {}
  allTickets.forEach(t => {
    const col = allColumns.find(c => c.id === t.column_id)
    const name = col ? col.name : '未分類'
    counts[name] = (counts[name] || 0) + 1
  })

  return {
    labels: Object.keys(counts),
    datasets: [{
      data: Object.values(counts),
      backgroundColor: ['#64748b', '#3b82f6', '#22c55e', '#ef4444', '#eab308', '#8b5cf6'],
      borderWidth: 0
    }]
  }
})

// 優先級分佈長條圖
const priorityChartData = computed(() => ({
  labels: ['高', '中', '低'],
  datasets: [{
    label: '任務數量',
    data: [stats.value.highPriority, stats.value.mediumPriority, stats.value.lowPriority],
    backgroundColor: ['#ef4444', '#eab308', '#64748b'],
    borderRadius: 6
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: '#94a3b8', padding: 16 }
    }
  }
}

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
    y: { ticks: { color: '#94a3b8', stepSize: 1 }, grid: { color: '#334155' } }
  }
}
</script>

<template>
  <div>
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
      <svg class="animate-spin h-10 w-10 text-blue-500 mb-4" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
      <p class="text-slate-400">彙總數據中...</p>
    </div>
    <div v-else>
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-white">📊 全站統計</h1>
      <p class="text-slate-400 mt-1">所有看板的彙總數據</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center text-2xl">📋</div>
          <div>
            <div class="text-2xl font-bold text-white">{{ stats.totalBoards }}</div>
            <div class="text-sm text-slate-400">看板數量</div>
          </div>
        </div>
      </div>

      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center text-2xl">📝</div>
          <div>
            <div class="text-2xl font-bold text-white">{{ stats.totalTickets }}</div>
            <div class="text-sm text-slate-400">總任務數</div>
          </div>
        </div>
      </div>

      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center text-2xl">✅</div>
          <div>
            <div class="text-2xl font-bold text-white">{{ completionRate }}%</div>
            <div class="text-sm text-slate-400">完成率</div>
          </div>
        </div>
      </div>

      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-yellow-500/20 flex items-center justify-center text-2xl">👥</div>
          <div>
            <div class="text-2xl font-bold text-white">{{ stats.totalUsers }}</div>
            <div class="text-sm text-slate-400">用戶數量</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h2 class="text-lg font-semibold text-white mb-4">狀態分佈</h2>
        <div class="h-64">
          <Doughnut :data="statusChartData" :options="chartOptions" />
        </div>
      </div>

      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h2 class="text-lg font-semibold text-white mb-4">優先級分佈</h2>
        <div class="h-64">
          <Bar :data="priorityChartData" :options="barOptions" />
        </div>
      </div>
    </div>

    <!-- Board Progress -->
    <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
      <h2 class="text-lg font-semibold text-white mb-4">各看板進度</h2>
      <div class="space-y-4">
        <div v-for="board in boardStats" :key="board.id" class="flex items-center gap-4">
          <div class="w-32 truncate text-slate-300 font-medium">{{ board.name }}</div>
          <div class="flex-1">
            <div class="h-3 bg-slate-700 rounded-full overflow-hidden">
              <div
                class="h-full bg-gradient-to-r from-blue-500 to-blue-400 rounded-full transition-all duration-300"
                :style="{ width: `${board.progress}%` }"
              ></div>
            </div>
          </div>
          <div class="w-20 text-right text-sm text-slate-400">
            {{ board.done }}/{{ board.total }} ({{ board.progress }}%)
          </div>
        </div>

        <div v-if="boardStats.length === 0" class="text-center py-8 text-slate-400">
          暫無看板資料
        </div>
      </div>
    </div>
    </div>
  </div>
</template>
