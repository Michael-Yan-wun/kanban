<script setup>
defineProps({
  ticket: {
    type: Object,
    required: true
  },
  columns: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['move', 'delete'])

const priorityColors = {
  low: 'bg-slate-500',
  medium: 'bg-yellow-500',
  high: 'bg-red-500'
}

const priorityLabels = {
  low: '低',
  medium: '中',
  high: '高'
}
</script>

<template>
  <div class="bg-slate-700/50 rounded-lg p-4 border border-slate-600/50 hover:border-indigo-500/50 transition-all duration-200 group">
    <!-- Priority Badge -->
    <div class="flex items-center justify-between mb-2">
      <span
        :class="['text-xs px-2 py-0.5 rounded-full text-white', priorityColors[ticket.priority]]"
      >
        {{ priorityLabels[ticket.priority] }}
      </span>
      <button
        @click="emit('delete', ticket.id)"
        class="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-red-400 transition-all"
        title="刪除"
      >
        🗑️
      </button>
    </div>

    <!-- Title -->
    <h3 class="font-medium text-white mb-1">{{ ticket.title }}</h3>
    
    <!-- Description -->
    <p class="text-sm text-slate-400 mb-3">{{ ticket.description }}</p>

    <!-- Move Actions -->
    <div class="flex gap-1 flex-wrap">
      <button
        v-for="col in columns.filter(c => c.id !== ticket.status)"
        :key="col.id"
        @click="emit('move', ticket.id, col.id)"
        class="text-xs px-2 py-1 bg-slate-600 hover:bg-slate-500 rounded text-slate-300 transition-colors"
      >
        → {{ col.title }}
      </button>
    </div>
  </div>
</template>
