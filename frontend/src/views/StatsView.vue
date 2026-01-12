<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
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

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, BarElement)

const route = useRoute()
const router = useRouter()
const boardStore = useBoardStore()
const ticketStore = useTicketStore()

const boardId = computed(() => parseInt(route.params.id))
const board = computed(() => boardStore.allBoards.find(b => b.id === boardId.value))

// 該看板的票券
const tickets = computed(() => ticketStore.getTicketsByBoard(boardId.value))

// 統計數據
const stats = computed(() => ({
  total: tickets.value.length,
  todo: tickets.value.filter(t => t.status === 'todo').length,
  inProgress: tickets.value.filter(t => t.status === 'inProgress').length,
  done: tickets.value.filter(t => t.status === 'done').length,
  high: tickets.value.filter(t => t.priority === 'high').length,
  medium: tickets.value.filter(t => t.priority === 'medium').length,
  low: tickets.value.filter(t => t.priority === 'low').length
}))

const completionRate = computed(() => {
  if (stats.value.total === 0) return 0
  return Math.round((stats.value.done / stats.value.total) * 100)
})

// 狀態分佈圓餅圖
const statusChartData = computed(() => ({
  labels: ['待辦事項', '進行中', '已完成'],
  datasets: [{
    data: [stats.value.todo, stats.value.inProgress, stats.value.done],
    backgroundColor: ['#64748b', '#3b82f6', '#22c55e'],
    borderWidth: 0
  }]
}))

// 優先級分佈長條圖
const priorityChartData = computed(() => ({
  labels: ['高', '中', '低'],
  datasets: [{
    label: '任務數量',
    data: [stats.value.high, stats.value.medium, stats.value.low],
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
  <div v-if="board">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center gap-3 mb-2">
        <button
          @click="router.push(`/boards/${boardId}`)"
          class="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
          title="返回看板"
        >
          ←
        </button>
        <h1 class="text-2xl font-bold text-white">📊 {{ board.name }} - 統計報表</h1>
      </div>
      <p class="text-slate-400 ml-11">{{ board.description }}</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div class="text-slate-400 text-sm mb-2">總任務數</div>
        <div class="text-3xl font-bold text-white">{{ stats.total }}</div>
      </div>
      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div class="text-slate-400 text-sm mb-2">待辦事項</div>
        <div class="text-3xl font-bold text-slate-400">{{ stats.todo }}</div>
      </div>
      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div class="text-slate-400 text-sm mb-2">進行中</div>
        <div class="text-3xl font-bold text-blue-400">{{ stats.inProgress }}</div>
      </div>
      <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div class="text-slate-400 text-sm mb-2">已完成</div>
        <div class="text-3xl font-bold text-green-400">{{ stats.done }}</div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50 mb-8">
      <div class="flex justify-between text-sm text-slate-400 mb-2">
        <span>整體完成進度</span>
        <span>{{ completionRate }}%</span>
      </div>
      <div class="h-4 bg-slate-700 rounded-full overflow-hidden">
        <div
          class="h-full bg-gradient-to-r from-blue-500 to-blue-400 rounded-full transition-all duration-500"
          :style="{ width: `${completionRate}%` }"
        ></div>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
  </div>

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
