<template>
  <div class="min-h-screen text-slate-100">
    <div class="fixed inset-0 bg-linear-to-br from-slate-900 via-slate-800 to-slate-900 -z-10" />
    
    <div class="relative container mx-auto px-4 py-12 max-w-6xl">
      <!-- Header -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center gap-2 px-4 py-2 glass rounded-full mb-4">
          <span class="text-sm text-blue-400 font-medium">✨ AI-Powered Analytics</span>
        </div>
        <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">
          Превратите данные в <span class="text-transparent bg-clip-text bg-linear-to-r from-blue-400 to-purple-400">историю</span>
        </h1>
        <p class="text-slate-400 max-w-2xl mx-auto text-lg">
          Загрузите CSV, Excel или текст, и получите мгновенные AI-инсайты, визуализацию и умный чат.
        </p>
      </div>

      <!-- Upload Zone -->
      <UploadZone @data-loaded="handleDataLoaded" />

      <!-- Dashboard -->
      <div v-if="data.length > 0 && analysis" class="mt-12 space-y-8 animate-fade-in">
        
        <!-- 1. AI Insight -->
        <div class="glass rounded-2xl p-6 border-l-4 border-l-blue-500">
          <div class="flex items-start gap-4">
            <div class="p-3 bg-blue-500/20 rounded-xl shrink-0">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            <div class="flex-1">
              <h2 class="text-sm font-semibold text-blue-400 uppercase tracking-wider mb-2">Главный инсайт</h2>
              <p class="text-xl leading-relaxed text-white/90">{{ analysis.insight }}</p>
              <div class="flex flex-wrap gap-4 mt-4 text-sm text-slate-400">
                <span class="glass px-3 py-1 rounded-full">📊 {{ data.length }} записей</span>
                <span class="glass px-3 py-1 rounded-full">📋 {{ headers.length }} полей</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. Chart Widget -->
        <ChartWidget 
          v-if="analysis.chart_data" 
          :chart-type="analysis.chart_type" 
          :chart-data="analysis.chart_data" 
        />

        <!-- 3. Recommendations -->
        <div v-if="analysis.recommendations && analysis.recommendations.length > 0" class="glass rounded-2xl p-6">
          <h3 class="text-lg font-semibold text-white mb-3 flex items-center gap-2">💡 Рекомендации</h3>
          <ul class="space-y-2">
            <li v-for="(rec, index) in analysis.recommendations" :key="index" class="text-slate-300 flex items-start gap-2">
              <span class="text-blue-400 mt-1">•</span> {{ rec }}
            </li>
          </ul>
        </div>

        <!-- 4. Chat with Data -->
        <div class="glass rounded-2xl p-6">
          <h3 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <span>💬</span> Спроси что-нибудь про эти данные
          </h3>
          
          <div class="space-y-4 max-h-80 overflow-y-auto mb-4 pr-2 custom-scrollbar" ref="chatContainer">
            <div v-if="chatMessages.length === 0" class="text-center text-slate-500 py-8 italic">
              Задайте вопрос, например: "Какая средняя сумма?" или "Покажи топ-3 категории"
            </div>
            <div v-for="(msg, idx) in chatMessages" :key="idx" class="flex gap-3" :class="msg.role === 'user' ? 'flex-row-reverse' : ''">
              <div class="p-3 rounded-2xl max-w-[85%] text-sm leading-relaxed"
                :class="msg.role === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 'bg-slate-700/50 text-slate-200 rounded-bl-none border border-slate-600/50'">
                {{ msg.content }}
              </div>
            </div>
            <div v-if="isChatLoading" class="flex gap-3">
              <div class="p-3 rounded-2xl bg-slate-700/50 text-slate-400 text-sm">
                <span class="animate-pulse">Думаю...</span>
              </div>
            </div>
          </div>
          
          <div class="flex gap-3">
            <input
              v-model="chatInput"
              @keyup.enter="sendMessage"
              placeholder="Напишите ваш вопрос..."
              class="flex-1 px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder:text-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all"
              :disabled="isChatLoading"
            />
            <button
              @click="sendMessage"
              :disabled="!chatInput.trim() || isChatLoading"
              class="px-6 py-3 bg-linear-to-r from-blue-600 to-purple-600 rounded-xl text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-blue-500/25 transition-all active:scale-95"
            >
              <span v-if="isChatLoading"></span>
              <span v-else>➤</span>
            </button>
          </div>
        </div>

        <!-- 5. Data Table Preview -->
        <div class="glass rounded-2xl p-6">
          <h3 class="text-lg font-semibold text-white mb-4">📑 Предпросмотр данных</h3>
          <div class="overflow-x-auto rounded-lg border border-slate-700/50">
            <table class="w-full text-slate-300 text-sm">
              <thead class="bg-slate-800/50 text-slate-400 uppercase text-xs">
                <tr>
                  <th v-for="key in headers" :key="key" class="text-left py-3 px-4 font-medium">{{ key }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-700/50">
                <tr v-for="(row, index) in data.slice(0, 8)" :key="index" class="hover:bg-slate-800/30 transition-colors">
                  <td v-for="key in headers" :key="key" class="py-3 px-4">{{ row[key] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-if="data.length > 8" class="text-slate-500 text-xs mt-3 text-center">
            ...и еще {{ data.length - 8 }} записей
          </p>
        </div>

      </div>

      <!-- Footer -->
      <div class="mt-16 text-center text-slate-600 text-sm">
        🔒 Данные обрабатываются в реальном времени и не сохраняются на сервере
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import UploadZone from './components/UploadZone.vue'
import ChartWidget from './components/ChartWidget.vue'
import { chatWith } from './api/client'

const data = ref([])
const analysis = ref(null)
const chatMessages = ref([])
const chatInput = ref('')
const isChatLoading = ref(false)
const chatContainer = ref(null)

const headers = computed(() => {
  if (!data.value || data.value.length === 0) return []
  return Object.keys(data.value[0])
})

const handleDataLoaded = (loadedData, analysisResult) => {
  data.value = loadedData
  analysis.value = analysisResult
  chatMessages.value = []
}

const sendMessage = async () => {
  if (!chatInput.value.trim() || !data.value.length) return
  
  const userMessage = chatInput.value
  chatMessages.value.push({ role: 'user', content: userMessage })
  chatInput.value = ''
  isChatLoading.value = true
  
  await nextTick()
  if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight

  try {
    const response = await chatWith(userMessage, data.value, '')
    chatMessages.value.push({ role: 'assistant', content: response.reply })
  } catch (err) {
    chatMessages.value.push({ role: 'assistant', content: '❌ Ошибка при получении ответа от AI. Проверьте подключение.' })
  } finally {
    isChatLoading.value = false
    await nextTick()
    if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
.animate-fade-in { animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>