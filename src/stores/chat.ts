import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Message, Conversation, ChatRequest, ChatResponse, Memory } from '@/types'
import { chatApi, memosApi } from '@/services/api'

export const useChatStore = defineStore('chat', () => {
  // State
  const currentConversation = ref<Conversation | null>(null)
  const messages = ref<Message[]>([])
  const isLoading = ref(false)
  const memories = ref<Memory[]>([])
  const memoryUsed = ref<boolean>(false)
  // MemOS 使用后端代理，不在前端直接初始化 SDK

  // Getters
  const conversationMessages = computed(() => {
    if (!currentConversation.value) return []
    return messages.value.filter(msg => msg.conversation_id === currentConversation.value?.conversation_id)
  })

  const hasMemories = computed(() => memories.value.length > 0)

  // Actions
  const startNewConversation = (userId: string) => {
    const conversationId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    currentConversation.value = {
      conversation_id: conversationId,
      user_id: userId,
      title: '新对话',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    messages.value = []
    memories.value = []
    memoryUsed.value = false

    // Persist conversation id
    localStorage.setItem('current_conversation_id', conversationId)
  }

  const initializeMemOS = (_config: { apiKey: string; baseURL: string }) => {
    return true
  }

  const searchMemories = async (query: string, userId: string, _limit = 5) => {
    try {
      const res = await memosApi.searchMemory(query, userId, currentConversation.value?.conversation_id)
      if (res.success) {
        return (res.data as unknown as Memory[]) || []
      }
      return []
    } catch (error) {
      console.error('Failed to search memories:', error)
      return []
    }
  }

  const storeMemory = async (content: string, userId: string, _metadata?: Record<string, any>) => {
    try {
      const messages = [
        { role: 'system', content: 'conversation snippet' },
        { role: 'assistant', content },
      ]
      await memosApi.addMessage(messages, userId, currentConversation.value?.conversation_id || '')
      return true
    } catch (error) {
      console.error('Failed to store memory:', error)
      return null
    }
  }

  const getRecentMemories = async (_userId: string, _limit = 5) => {
    return []
  }

  const sendMessage = async (userId: string, content: string, context?: Record<string, any>) => {
    if (!content.trim()) return

    isLoading.value = true

    try {
      // Search for relevant memories before sending message
      let relevantMemories: Memory[] = []
      try {
        relevantMemories = await searchMemories(content, userId, 3)
      } catch (error) {
        console.warn('Failed to search memories:', error)
      }

      // Add user message to local state
      const userMessage: Message = {
        message_id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        conversation_id: currentConversation.value?.conversation_id || '',
        sender_type: 'user',
        content: content.trim(),
        timestamp: new Date().toISOString()
      }
      messages.value.push(userMessage)

      // Prepare chat request with memory context
      const chatRequest: ChatRequest = {
        user_id: userId,
        message: content.trim(),
        context: {
          fitness_goal: context?.fitness_goal || 'general',
          experience_level: context?.experience_level || 'beginner',
          conversation_id: currentConversation.value?.conversation_id,
          relevant_memories: relevantMemories.map(m => ({
            id: m.id,
            content: m.content,
            timestamp: m.timestamp,
            relevance: m.relevance || 0.8
          })),
          ...context
        }
      }

      // Send message to API
      const response = await chatApi.sendMessage(chatRequest)
      
      if (response.success) {
        const chatResponse = response.data
        
        // Add AI response to local state
        const aiMessage: Message = {
          message_id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          conversation_id: currentConversation.value?.conversation_id || '',
          sender_type: 'assistant',
          content: chatResponse.reply,
          timestamp: new Date().toISOString(),
          metadata: {
            memory_used: chatResponse.memory_used,
            related_memories: chatResponse.related_memories
          }
        }
        messages.value.push(aiMessage)

        // Update memories
        memories.value = chatResponse.related_memories || []
        memoryUsed.value = chatResponse.memory_used

        // Store important information as memory
        if (shouldStoreAsMemory(content, chatResponse.reply)) {
          try {
            await storeMemory(
              `User: ${content}\nAssistant: ${chatResponse.reply}`,
              userId,
              {
                type: 'conversation',
                conversationId: currentConversation.value?.conversation_id,
                timestamp: new Date().toISOString(),
                userMessage: content,
                assistantReply: chatResponse.reply
              }
            )
          } catch (error) {
            console.warn('Failed to store memory:', error)
          }
        }

        // Update conversation title if it's the first message
        if (messages.value.length === 2) {
          updateConversationTitle(content.trim())
        }
      } else {
        throw new Error(response.message || '发送消息失败')
      }
    } catch (error) {
      console.error('发送消息失败:', error)
      // Remove the user message if API call failed
      messages.value.pop()
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const updateConversationTitle = (firstMessage: string) => {
    if (currentConversation.value) {
      const title = firstMessage.length > 20 
        ? firstMessage.substring(0, 20) + '...' 
        : firstMessage
      currentConversation.value.title = title
      currentConversation.value.updated_at = new Date().toISOString()
    }
  }

  const clearMessages = () => {
    messages.value = []
    memories.value = []
    memoryUsed.value = false
  }

  const loadConversation = (conversation: Conversation) => {
    currentConversation.value = conversation
    messages.value = []
    memories.value = []
    memoryUsed.value = false

    // Load history from API
    ;(async () => {
      try {
        const res = await chatApi.getConversationHistory(conversation.conversation_id)
        if (res.success && (res.data as any)?.messages) {
          const list = (res.data as any).messages as Array<any>
          for (const m of list) {
            messages.value.push({
              message_id: m.message_id || `msg_${Math.random()}`,
              conversation_id: conversation.conversation_id,
              sender_type: m.sender_type,
              content: m.content,
              timestamp: m.timestamp,
            })
          }
        }
      } catch (e) {
        console.warn('加载历史消息失败', e)
      }
    })()

    // Persist
    localStorage.setItem('current_conversation_id', conversation.conversation_id)
  }

  // Helper function to determine if content should be stored as memory
  const shouldStoreAsMemory = (userMessage: string, assistantReply: string): boolean => {
    // Store as memory if the conversation contains important fitness-related information
    const importantKeywords = [
      'weight', '身高', '体重', '目标', '计划', '训练', '饮食', 
      '习惯', '偏好', '目标', '体重', '身高', '年龄', '性别'
    ]
    
    const combinedContent = `${userMessage} ${assistantReply}`.toLowerCase()
    return importantKeywords.some(keyword => combinedContent.includes(keyword))
  }

  return {
    // State
    currentConversation,
    messages,
    isLoading,
    memories,
    memoryUsed,
    
    // Getters
    conversationMessages,
    hasMemories,
    
    // Actions
    startNewConversation,
    sendMessage,
    clearMessages,
    loadConversation,
    // Hydrate from localStorage
    hydrate() {
      const cid = localStorage.getItem('current_conversation_id')
      const uid = localStorage.getItem('user_id') || 'fitness_user_123'
      if (cid) {
        currentConversation.value = {
          conversation_id: cid,
          user_id: uid,
          title: '新对话',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }
      }
    },
    initializeMemOS,
    searchMemories,
    storeMemory,
    getRecentMemories
  }
})
