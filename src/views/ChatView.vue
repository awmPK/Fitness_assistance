<template>
  <div class="h-screen flex flex-col bg-gradient-to-br from-gray-50 to-gray-100 chat-container">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
            <el-icon class="text-white text-lg">
              <Avatar />
            </el-icon>
          </div>
          <div>
            <h1 class="text-lg font-semibold text-gray-900">AI健身助手</h1>
            <p class="text-sm text-gray-500">您的专属健身伙伴</p>
          </div>
        </div>
        
        <div class="flex items-center gap-2">
          <!-- Memory indicator -->
          <div 
            v-if="chatStore.hasMemories"
            class="flex items-center gap-1 px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-xs"
          >
            <el-icon><Memo /></el-icon>
            <span>记忆活跃</span>
          </div>
          
          <!-- History button -->
          <el-button
            @click="showHistory = true; loadConversations()"
            size="small"
            round
          >
            历史会话
          </el-button>

          <!-- New conversation button -->
          <el-button
            type="primary"
            :icon="Plus"
            @click="startNewConversation"
            size="small"
            round
          >
            新对话
          </el-button>
          
          <!-- Settings button -->
          <el-button
            circle
            :icon="Setting"
            @click="showSettings = true"
            size="small"
          />
        </div>
      </div>
    </div>

    <!-- Chat messages area -->
    <div class="flex-1 overflow-y-auto p-6" ref="messagesContainer">
      <!-- Welcome message -->
      <div v-if="chatStore.conversationMessages.length === 0" class="text-center py-12">
        <div class="max-w-md mx-auto">
          <div class="w-20 h-20 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center mx-auto mb-6">
            <el-icon class="text-white text-3xl">
              <Avatar />
            </el-icon>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-4">欢迎使用AI健身助手</h2>
          <p class="text-gray-600 mb-8">
            我是您的专属健身伙伴，可以为您制定个性化的健身计划、提供专业的训练建议，
            并通过记忆功能为您提供持续的个性化服务。
          </p>
          <div class="grid grid-cols-2 gap-3">
            <el-button 
              type="primary" 
              @click="sendQuickMessage('帮我制定一个减脂计划')"
              round
            >
              制定减脂计划
            </el-button>
            <el-button 
              @click="sendQuickMessage('我想增肌，有什么建议')"
              round
            >
              增肌训练建议
            </el-button>
          </div>
        </div>
      </div>

      <!-- Messages -->
      <div v-else class="space-y-4">
        <ChatMessage
          v-for="message in chatStore.conversationMessages"
          :key="message.message_id"
          :message="message"
        />
      </div>

      <!-- Loading indicator -->
      <div v-if="chatStore.isLoading" class="flex justify-center py-4">
        <div class="flex items-center gap-2 text-gray-500">
          <el-icon class="animate-spin">
            <Loading />
          </el-icon>
          <span>AI正在思考...</span>
        </div>
      </div>
    </div>

    <!-- Memory panel (collapsible) -->
    <div 
      v-if="chatStore.hasMemories" 
      class="bg-primary-50 border-t border-primary-200 p-4"
    >
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2">
          <el-icon class="text-primary-600"><Memo /></el-icon>
          <span class="text-sm font-medium text-primary-800">相关记忆</span>
        </div>
        <el-button
          text
          size="small"
          @click="showMemories = !showMemories"
        >
          {{ showMemories ? '收起' : '展开' }}
        </el-button>
      </div>
      
      <el-collapse-transition>
        <div v-show="showMemories">
          <div class="space-y-2">
            <div 
              v-for="(memory, index) in chatStore.memories" 
              :key="index"
              class="bg-white rounded-lg p-3 text-sm text-gray-700 border border-primary-200"
            >
              <div class="font-medium text-gray-900 mb-1">记忆 {{ index + 1 }}</div>
              <div class="text-gray-600">{{ memory.content }}</div>
              <div class="text-xs text-gray-400 mt-1">
                相关性: {{ Math.round((memory.relevance || 0.8) * 100) }}%
              </div>
            </div>
          </div>
        </div>
      </el-collapse-transition>
    </div>

    <!-- Chat input -->
    <div class="chat-input-container">
      <ChatInput
        :is-loading="chatStore.isLoading"
        @send="handleSendMessage"
      />
    </div>

    <!-- Settings dialog -->
    <el-dialog
      v-model="showSettings"
      title="设置"
      width="400px"
      :close-on-click-modal="false"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">语音输入语言</label>
          <el-select v-model="voiceLanguage" class="w-full">
            <el-option label="中文" value="zh-CN" />
            <el-option label="English" value="en-US" />
          </el-select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">回复语音播报</label>
          <el-switch v-model="enableVoiceReply" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">记忆功能</label>
          <el-switch v-model="enableMemory" />
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showSettings = false">取消</el-button>
        <el-button type="primary" @click="saveSettings">保存</el-button>
      </template>
    </el-dialog>

    <!-- History Drawer -->
    <el-drawer v-model="showHistory" title="历史会话" size="30%">
      <div class="space-y-2">
        <div v-if="conversations.length === 0" class="text-sm text-gray-500">暂无历史会话</div>
        <div v-else class="space-y-2">
          <el-button
            v-for="conv in conversations"
            :key="conv.conversation_id"
            @click="selectConversation(conv)"
            class="w-full text-left"
            style="justify-content: flex-start; padding: 8px;"
            plain
            type="default"
          >
            <div class="w-full">
              <div class="text-sm text-gray-900 truncate">{{ conv.title || '新对话' }}</div>
              <div class="text-xs text-gray-400">{{ conv.conversation_id }}</div>
            </div>
          </el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useChatStore } from '@/stores/chat'
import { useUserStore } from '@/stores/user'
import ChatMessage from '@/components/Chat/ChatMessage.vue'
import ChatInput from '@/components/Chat/ChatInput.vue'
import { Avatar, Memo, Plus, Setting, Loading } from '@element-plus/icons-vue'
import { chatApi } from '@/services/api'

// Store
const chatStore = useChatStore()
const userStore = useUserStore()

// 从 userStore 获取实际用户ID
const userId = computed(() => userStore.user?.user_id || localStorage.getItem('user_id') || '')

// Refs
const messagesContainer = ref<HTMLElement>()
const showSettings = ref(false)
const showMemories = ref(true)
const showHistory = ref(false)
const conversations = ref<Array<{ conversation_id: string; title: string }>>([])

// Settings
const voiceLanguage = ref('zh-CN')
const enableVoiceReply = ref(false)
const enableMemory = ref(true)

// Methods
const startNewConversation = () => {
  if (!userId.value) {
    ElMessage.error('请先登录')
    return
  }
  chatStore.startNewConversation(userId.value)
  ElMessage.success('开始新的对话')
  loadConversations()
}

const selectConversation = async (conv: { conversation_id: string; title: string }) => {
  console.log('selectConversation clicked', conv)
  chatStore.loadConversation({
    conversation_id: conv.conversation_id,
    user_id: userId.value,
    title: conv.title,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  })
  try {
    const res = await chatApi.getConversationHistory(conv.conversation_id)
    if (res.success && (res.data as any)?.messages) {
      chatStore.clearMessages()
      const list = (res.data as any).messages as Array<any>
      for (const m of list) {
        chatStore.messages.push({
          message_id: m.message_id || `msg_${Math.random()}`,
          conversation_id: conv.conversation_id,
          sender_type: m.sender_type,
          content: m.content,
          timestamp: m.timestamp,
        })
      }
    }
  } catch (e) {
    console.warn('加载历史消息失败', e)
  }
  showHistory.value = false
  ElMessage.success('已切换到历史会话')
}

const loadConversations = async () => {
  if (!userId.value) return
  try {
    const res = await chatApi.getConversations(userId.value)
    if (res.success) {
      conversations.value = (res.data as any) || []
    }
  } catch (e) {
    console.warn('加载历史会话失败', e)
  }
}



const handleSendMessage = async (message: string) => {
  if (!userId.value) {
    ElMessage.error('请先登录')
    return
  }
  try {
    await chatStore.sendMessage(userId.value, message, {
      fitness_goal: 'general',
      experience_level: 'beginner',
      enable_memory: enableMemory.value
    })
    
    // Scroll to bottom
    await nextTick()
    scrollToBottom()
    
    // Voice reply if enabled
    if (enableVoiceReply.value && chatStore.conversationMessages.length > 0) {
      const lastMessage = chatStore.conversationMessages[chatStore.conversationMessages.length - 1]
      if (lastMessage.sender_type === 'assistant') {
        speakText(lastMessage.content)
      }
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送消息失败，请重试')
  }
}

const sendQuickMessage = (message: string) => {
  handleSendMessage(message)
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const saveSettings = () => {
  localStorage.setItem('chat_settings', JSON.stringify({
    voiceLanguage: voiceLanguage.value,
    enableVoiceReply: enableVoiceReply.value,
    enableMemory: enableMemory.value
  }))
  showSettings.value = false
  ElMessage.success('设置已保存')
}

const speakText = (text: string) => {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = voiceLanguage.value
    utterance.rate = 0.9
    utterance.pitch = 1
    speechSynthesis.speak(utterance)
  }
}

// Load settings on mount
onMounted(async () => {
  // 先加载用户信息
  if (!userStore.user) {
    await userStore.loadUser()
  }
  
  const savedSettings = localStorage.getItem('chat_settings')
  if (savedSettings) {
    try {
      const settings = JSON.parse(savedSettings)
      voiceLanguage.value = settings.voiceLanguage || 'zh-CN'
      enableVoiceReply.value = settings.enableVoiceReply || false
      enableMemory.value = settings.enableMemory !== false
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  }
  
  // Hydrate existing conversation if any
  chatStore.hydrate()
  if (!chatStore.currentConversation && userId.value) {
    chatStore.startNewConversation(userId.value)
  }
  loadConversations()
})
</script>

<style scoped>
/* Custom scrollbar for messages area */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Animation for new messages */
:deep(.animate-fade-in) {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
