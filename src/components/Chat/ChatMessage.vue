<template>
  <div 
    :class="[
      'flex mb-4 animate-fade-in',
      message.sender_type === 'user' ? 'justify-end' : 'justify-start'
    ]"
  >
    <div 
      :class="[
        'max-w-[85%] md:max-w-[70%] rounded-2xl px-4 py-3 shadow-sm',
        'transition-all duration-200 hover:shadow-md',
        message.sender_type === 'user' 
          ? 'bg-primary-500 text-white rounded-br-md' 
          : 'bg-white text-gray-800 rounded-bl-md border border-gray-200'
      ]"
    >
      <div class="flex items-start gap-2">
        <!-- Avatar -->
        <div 
          v-if="message.sender_type === 'assistant'"
          class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center flex-shrink-0"
        >
          <el-icon class="text-white text-sm">
            <Avatar />
          </el-icon>
        </div>
        
        <div class="flex-1 min-w-0">
          <!-- Message content -->
          <div 
            class="text-sm md:text-base leading-relaxed whitespace-pre-wrap mobile-text-sm"
            v-html="formattedContent"
          ></div>
          
          <!-- Timestamp -->
          <div 
            :class="[
              'text-xs mt-2 opacity-70',
              message.sender_type === 'user' ? 'text-right' : 'text-left'
            ]"
          >
            {{ formatTime(message.timestamp) }}
          </div>
          
          <!-- Memory indicator -->
          <div 
            v-if="message.metadata?.memory_used && message.sender_type === 'assistant'"
            class="mt-2 flex items-center gap-1 text-xs text-primary-600"
          >
            <el-icon><Memo /></el-icon>
            <span>基于记忆回复</span>
          </div>
        </div>
        
        <!-- User avatar -->
        <div 
          v-if="message.sender_type === 'user'"
          class="w-8 h-8 rounded-full bg-gradient-to-br from-secondary-500 to-primary-500 flex items-center justify-center flex-shrink-0"
        >
          <el-icon class="text-white text-sm">
            <User />
          </el-icon>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Message } from '@/types'
import { ElIcon } from 'element-plus'
import { Avatar, User, Memo } from '@element-plus/icons-vue'

interface Props {
  message: Message
}

const props = defineProps<Props>()

const formattedContent = computed(() => {
  // Simple markdown-like formatting
  let content = props.message.content
  
  // Convert URLs to links
  content = content.replace(
    /(https?:\/\/[^\s]+)/g,
    '<a href="$1" target="_blank" class="text-blue-500 hover:text-blue-700 underline">$1</a>'
  )
  
  // Convert **text** to bold
  content = content.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  
  // Convert *text* to italic
  content = content.replace(/\*([^*]+)\*/g, '<em>$1</em>')
  
  // Convert line breaks to <br> tags
  content = content.replace(/\n/g, '<br>')
  
  return content
})

const formatTime = (timestamp: string): string => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  // Less than 1 minute
  if (diff < 60000) {
    return '刚刚'
  }
  
  // Less than 1 hour
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes}分钟前`
  }
  
  // Less than 24 hours
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}小时前`
  }
  
  // More than 24 hours
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
/* Custom animations */
.animate-fade-in {
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

/* Ensure links in messages are visible */
:deep(a) {
  color: inherit;
  text-decoration: underline;
  opacity: 0.9;
}

:deep(a:hover) {
  opacity: 1;
}

/* User message link styling */
.bg-primary-500 :deep(a) {
  color: #e0e7ff;
  text-decoration: underline;
}

.bg-primary-500 :deep(a:hover) {
  color: #ffffff;
}
</style>