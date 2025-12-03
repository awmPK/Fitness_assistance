<template>
  <div class="border-t border-gray-200 bg-white p-4">
    <!-- Quick suggestions -->
    <div class="mb-3 flex flex-wrap gap-2">
      <el-button
        v-for="suggestion in quickSuggestions"
        :key="suggestion"
        size="small"
        round
        @click="handleQuickSuggestion(suggestion)"
        class="text-xs"
      >
        {{ suggestion }}
      </el-button>
    </div>

    <!-- Input area -->
    <div class="flex items-end gap-3">
      <!-- Voice input button -->
      <el-button
        circle
        :type="isRecording ? 'danger' : 'primary'"
        :icon="isRecording ? Microphone : Phone"
        @click="toggleVoiceInput"
        :loading="isProcessingVoice"
        size="large"
        class="flex-shrink-0"
      />
      
      <!-- Text input -->
      <div class="flex-1 relative">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="1"
          :autosize="{ minRows: 1, maxRows: 4 }"
          placeholder="输入您的健身问题或需求..."
          @keydown.enter.prevent="handleSend"
          @keydown.enter.ctrl.prevent="addNewline"
          class="chat-input"
          :disabled="isLoading"
        />
        
        <!-- Character count -->
        <div 
          v-if="inputText.length > 0"
          class="absolute bottom-2 right-3 text-xs text-gray-400"
        >
          {{ inputText.length }}/500
        </div>
      </div>
      
      <!-- Send button -->
      <el-button
        type="primary"
        :icon="Position"
        @click="handleSend"
        :loading="isLoading"
        :disabled="!canSend"
        size="large"
        class="flex-shrink-0"
        round
      >
        发送
      </el-button>
    </div>

    <!-- Voice input status -->
    <div 
      v-if="isRecording || isProcessingVoice"
      class="mt-3 flex items-center gap-2 text-sm text-gray-600"
    >
      <el-icon 
        v-if="isRecording" 
        class="animate-pulse text-red-500"
      >
        <Microphone />
      </el-icon>
      <el-icon 
        v-else-if="isProcessingVoice" 
        class="animate-spin"
      >
        <Loading />
      </el-icon>
      <span>{{ voiceStatusText }}</span>
    </div>

    <!-- Input tips -->
    <div class="mt-2 text-xs text-gray-500">
      按 Enter 发送消息，Ctrl+Enter 换行
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Position, Microphone, Phone, Loading } from '@element-plus/icons-vue'

interface Props {
  isLoading?: boolean
}

interface Emits {
  (e: 'send', message: string): void
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false
})

const emit = defineEmits<Emits>()

// State
const inputText = ref('')
const isRecording = ref(false)
const isProcessingVoice = ref(false)

// Quick suggestions
const quickSuggestions = [
  '制定减脂计划',
  '增肌训练建议',
  '今日训练安排',
  '饮食营养指导',
  '运动损伤预防',
  '训练强度调整'
]

// Computed
const canSend = computed(() => {
  return inputText.value.trim().length > 0 && !props.isLoading && !isRecording.value && !isProcessingVoice.value
})

const voiceStatusText = computed(() => {
  if (isRecording.value) return '正在录音... 点击停止'
  if (isProcessingVoice) return '正在处理语音...'
  return ''
})

// Methods
const handleSend = () => {
  if (!canSend.value) return
  
  const message = inputText.value.trim()
  emit('send', message)
  inputText.value = ''
}

const addNewline = () => {
  inputText.value += '\n'
}

const handleQuickSuggestion = (suggestion: string) => {
  inputText.value = suggestion
  // Focus the input
  const input = document.querySelector('.chat-input textarea') as HTMLTextAreaElement
  if (input) {
    input.focus()
  }
}

const toggleVoiceInput = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

const startRecording = () => {
  // Check if browser supports speech recognition
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    ElMessage.warning('您的浏览器不支持语音识别功能')
    return
  }
  
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
  const recognition = new SpeechRecognition()
  
  recognition.lang = 'zh-CN'
  recognition.continuous = false
  recognition.interimResults = false
  
  recognition.onstart = () => {
    isRecording.value = true
    ElMessage.success('开始录音，请说话...')
  }
  
  recognition.onresult = (event: any) => {
    const transcript = event.results[0][0].transcript
    inputText.value = transcript
    ElMessage.success('语音识别完成')
  }
  
  recognition.onerror = (event: any) => {
    console.error('语音识别错误:', event.error)
    ElMessage.error('语音识别失败，请重试')
    isRecording.value = false
  }
  
  recognition.onend = () => {
    isRecording.value = false
  }
  
  try {
    recognition.start()
  } catch (error) {
    console.error('启动语音识别失败:', error)
    ElMessage.error('启动语音识别失败')
    isRecording.value = false
  }
}

const stopRecording = () => {
  // This would be called automatically by the recognition.onend event
  isRecording.value = false
}

// Speech synthesis for reading messages (optional feature)
const speakText = (text: string) => {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'zh-CN'
    utterance.rate = 0.9
    utterance.pitch = 1
    speechSynthesis.speak(utterance)
  }
}
</script>

<style scoped>
/* Custom styles for chat input */
:deep(.chat-input) {
  .el-textarea__inner {
    padding-right: 60px;
    border-radius: 1rem;
    border-color: #e5e7eb;
    transition: all 0.2s ease;
  }
  
  .el-textarea__inner:focus {
    border-color: #FF6B35;
    box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.1);
  }
  
  .el-textarea__inner:hover {
    border-color: #d1d5db;
  }
}

/* Button hover effects */
:deep(.el-button) {
  transition: all 0.2s ease;
}

:deep(.el-button:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Quick suggestion buttons */
:deep(.el-button--small) {
  border-radius: 9999px;
  padding: 6px 12px;
}
</style>