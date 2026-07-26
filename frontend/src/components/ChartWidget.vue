<template>
  <div class="glass rounded-2xl p-6">
    <h3 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
      <span>📊</span> Визуализация данных
    </h3>
    
    <div class="relative h-80 w-full">
      <Bar v-if="chartType === 'bar'" :data="chartDataComputed" :options="chartOptions" />
      <Line v-else-if="chartType === 'line'" :data="chartDataComputed" :options="chartOptions" />
      <Pie v-else-if="chartType === 'pie'" :data="chartDataComputed" :options="chartOptions" />
      
      <div v-else class="flex items-center justify-center h-full text-white/40">
        Нет данных для визуализации
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar, Line, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement,
  BarElement, ArcElement, Title, Tooltip, Legend
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend)

const props = defineProps({
  chartType: { type: String, default: 'bar' },
  chartData: { type: Object, default: () => ({ labels: [], datasets: [] }) }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: 'rgba(255, 255, 255, 0.8)' } },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      titleColor: '#fff',
      bodyColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
      padding: 10,
      cornerRadius: 8
    }
  },
  scales: {
    x: { ticks: { color: 'rgba(255, 255, 255, 0.6)' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
    y: { ticks: { color: 'rgba(255, 255, 255, 0.6)' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
  }
}

const chartDataComputed = computed(() => ({
  labels: props.chartData?.labels || [],
  datasets: (props.chartData?.datasets || []).map((dataset, index) => ({
    ...dataset,
    backgroundColor: ['rgba(59, 130, 246, 0.7)', 'rgba(168, 85, 247, 0.7)', 'rgba(236, 72, 153, 0.7)'][index % 3],
    borderColor: ['rgb(59, 130, 246)', 'rgb(168, 85, 247)', 'rgb(236, 72, 153)'][index % 3],
    borderWidth: 2,
    tension: 0.4,
    borderRadius: 4
  }))
}))
</script>