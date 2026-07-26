<template>
  <div class="w-full max-w-4xl mx-auto space-y-6">
    <div
      class="relative border-2 border-dashed rounded-2xl p-12 transition-all duration-300 glass glass-hover"
      :class="[
        isDragging ? 'border-blue-500 bg-blue-500/10 scale-[1.01]' : 'border-white/20',
        error ? 'border-red-500/50' : ''
      ]"
      @dragenter="isDragging = true"
      @dragleave="isDragging = false"
      @dragover.prevent
      @drop.prevent="handleDrop"
    >
      <div v-if="isLoading" class="text-center">
        <div class="w-12 h-12 mx-auto text-blue-400 animate-spin mb-4 border-4 border-blue-400 border-t-transparent rounded-full"></div>
        <div class="w-full max-w-xs mx-auto bg-white/10 rounded-full h-2 overflow-hidden">
          <div
            class="bg-linear-to-r from-blue-500 to-purple-500 h-full rounded-full transition-all duration-300"
            :style="{ width: progress + '%' }"
          />
        </div>
        <p class="text-white/60 mt-3">
          {{ progress < 100 ? 'Анализируем данные...' : 'Готово!' }}
        </p>
      </div>

      <div v-else-if="file && !isLoading" class="flex items-center justify-center gap-4">
        <div class="p-3 bg-blue-500/20 rounded-xl">
          <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div class="text-left">
          <p class="text-white/80 font-medium">{{ file.name }}</p>
          <p class="text-white/40 text-sm">{{ (file.size / 1024).toFixed(1) }} KB</p>
        </div>
        <button @click="clearFile" class="p-2 hover:bg-white/10 rounded-full transition-colors">
          <svg class="w-5 h-5 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div v-else class="text-center">
        <div class="w-20 h-20 mx-auto glass rounded-2xl flex items-center justify-center mb-4">
          <svg class="w-10 h-10 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-white/80">
          Перетащите файл сюда
        </h3>
        <p class="text-white/40 mt-2">
          Поддерживаются CSV, Excel (.xlsx, .xls)
        </p>
        <input
          ref="fileInput"
          type="file"
          accept=".csv,.xlsx,.xls"
          class="hidden"
          @change="handleFileSelect"
        />
        <button
          @click="$refs.fileInput.click()"
          class="mt-4 px-6 py-2 bg-linear-to-r from-blue-500 to-purple-500 rounded-lg text-white hover:shadow-lg hover:shadow-blue-500/25 transition-all"
        >
          Выбрать файл
        </button>
      </div>

      <p v-if="error" class="text-red-400 text-sm mt-4 text-center">
        {{ error }}
      </p>
    </div>

    <div class="relative glass rounded-xl">
      <div class="flex items-start gap-3 p-3">
        <svg class="w-5 h-5 text-white/30 mt-3 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <textarea
          v-model="textInput"
          placeholder="Или вставьте неструктурированный текст отчета..."
          class="flex-1 min-h-25 bg-transparent text-white placeholder:text-white/30 resize-none focus:outline-none"
          :disabled="isLoading"
        />
        <button
          @click="handleTextSubmit"
          :disabled="!textInput.trim() || isLoading"
          class="px-4 py-2 bg-linear-to-r from-blue-500 to-purple-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-blue-500/25 transition-all"
        >
          Анализировать
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { uploadFile, analyzeData } from '../api/client'

const emit = defineEmits(['data-loaded'])

const isDragging = ref(false)
const isLoading = ref(false)
const progress = ref(0)
const file = ref(null)
const textInput = ref('')
const error = ref(null)

const handleDrop = async (e) => {
  isDragging.value = false
  const droppedFile = e.dataTransfer.files[0]
  if (droppedFile) {
    await processFile(droppedFile)
  }
}

const handleFileSelect = async (e) => {
  const selectedFile = e.target.files[0]
  if (selectedFile) {
    await processFile(selectedFile)
  }
}

const processFile = async (selectedFile) => {
  file.value = selectedFile
  error.value = null
  isLoading.value = true
  progress.value = 0

  const interval = setInterval(() => {
    progress.value = Math.min(progress.value + 10, 90)
  }, 100)

  try {
    const result = await uploadFile(selectedFile)
    progress.value = 100
    
    const analysis = await analyzeData(result.preview)
    
    setTimeout(() => {
      emit('data-loaded', result.preview, analysis)
      isLoading.value = false
      clearInterval(interval)
    }, 500)
    
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки файла'
    isLoading.value = false
    clearInterval(interval)
  }
}

const clearFile = () => {
  file.value = null
  error.value = null
}

const handleTextSubmit = async () => {
  if (!textInput.value.trim()) return
  
  isLoading.value = true
  error.value = null
  
  try {
    const analysis = await analyzeData([], textInput.value)
    
    const lines = textInput.value.split('\n').filter(line => line.trim())
    const headers = lines[0].split(/\t|,|;/).map(h => h.trim())
    const data = lines.slice(1).map(line => {
      const values = line.split(/\t|,|;/).map(v => v.trim())
      const obj = {}
      headers.forEach((h, i) => {
        obj[h] = isNaN(Number(values[i])) ? values[i] : Number(values[i])
      })
      return obj
    })
    
    emit('data-loaded', data, analysis)
    textInput.value = ''
  } catch (err) {
    error.value = 'Ошибка анализа текста'
  } finally {
    isLoading.value = false
  }
}
</script>