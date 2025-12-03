import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { MemOSClient } from '@/services/memos'
import type { Memory, MemoryQuery } from '@/types'

export const useMemoryStore = defineStore('memory', () => {
  // State
  const enabled = ref(false)
  const showPanel = ref(true)
  const maxMemories = ref(5)
  const memories = ref<Memory[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  // MemOS client instance
  let memosClient: MemOSClient | null = null

  // Computed
  const hasMemories = computed(() => memories.value.length > 0)
  const recentMemories = computed(() => 
    memories.value.slice(0, maxMemories.value)
  )
  
  // Initialize MemOS client
  const initializeMemOS = () => {
    if (enabled.value && !memosClient) {
      try {
        memosClient = new MemOSClient({
          apiKey: import.meta.env.VITE_MEMOS_API_KEY || '',
          baseURL: import.meta.env.VITE_MEMOS_BASE_URL || 'http://localhost:8000',
          timeout: 30000
        })
      } catch (error) {
        console.error('Failed to initialize MemOS client:', error)
        setError('记忆服务初始化失败')
      }
    }
  }

  // Search memories
  const searchMemories = async (query: MemoryQuery) => {
    if (!enabled.value || !memosClient) {
      return []
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const results = await memosClient.search(query)
      memories.value = results
      return results
    } catch (error) {
      console.error('Failed to search memories:', error)
      setError('搜索记忆失败')
      return []
    } finally {
      isLoading.value = false
    }
  }

  // Store memory
  const storeMemory = async (content: string, metadata?: Record<string, any>) => {
    if (!enabled.value || !memosClient) {
      return null
    }
    
    try {
      const memory = await memosClient.store(content, metadata)
      
      // Add to local cache
      memories.value.unshift(memory)
      
      // Keep only recent memories
      if (memories.value.length > maxMemories.value * 2) {
        memories.value = memories.value.slice(0, maxMemories.value * 2)
      }
      
      return memory
    } catch (error) {
      console.error('Failed to store memory:', error)
      setError('存储记忆失败')
      return null
    }
  }

  // Update memory
  const updateMemory = async (id: string, content: string, metadata?: Record<string, any>) => {
    if (!enabled.value || !memosClient) {
      return null
    }
    
    try {
      const updated = await memosClient.update(id, content, metadata)
      
      // Update local cache
      const index = memories.value.findIndex(m => m.id === id)
      if (index !== -1) {
        memories.value[index] = updated
      }
      
      return updated
    } catch (error) {
      console.error('Failed to update memory:', error)
      setError('更新记忆失败')
      return null
    }
  }

  // Delete memory
  const deleteMemory = async (id: string) => {
    if (!enabled.value || !memosClient) {
      return false
    }
    
    try {
      await memosClient.delete(id)
      
      // Remove from local cache
      memories.value = memories.value.filter(m => m.id !== id)
      
      return true
    } catch (error) {
      console.error('Failed to delete memory:', error)
      setError('删除记忆失败')
      return false
    }
  }

  // Get memories for context
  const getContextMemories = async (context: string, limit = 5) => {
    if (!enabled.value) {
      return []
    }
    
    const userId = localStorage.getItem('user_id') || 'fitness_user_123'
    return searchMemories({
      query: context,
      limit,
      threshold: 0.7,
      userId
    })
  }

  // Clear memories
  const clearMemories = () => {
    memories.value = []
  }

  // Set error
  const setError = (message: string) => {
    error.value = message
    setTimeout(() => {
      error.value = null
    }, 5000)
  }

  // Toggle memory functionality
  const toggleMemory = () => {
    enabled.value = !enabled.value
    
    if (enabled.value) {
      initializeMemOS()
    } else {
      memosClient = null
      clearMemories()
    }
    
    saveSettings()
  }

  // Toggle memory panel
  const toggleMemoryPanel = () => {
    showPanel.value = !showPanel.value
    saveSettings()
  }

  // Set max memories
  const setMaxMemories = (value: number) => {
    maxMemories.value = Math.max(1, Math.min(10, value))
    
    // Trim memories if needed
    if (memories.value.length > maxMemories.value * 2) {
      memories.value = memories.value.slice(0, maxMemories.value * 2)
    }
    
    saveSettings()
  }

  // Save settings
  const saveSettings = () => {
    const settings = {
      enabled: enabled.value,
      showPanel: showPanel.value,
      maxMemories: maxMemories.value
    }
    localStorage.setItem('memory-settings', JSON.stringify(settings))
  }

  // Load settings
  const loadSettings = () => {
    try {
      const saved = localStorage.getItem('memory-settings')
      if (saved) {
        const settings = JSON.parse(saved)
        enabled.value = settings.enabled ?? false
        showPanel.value = settings.showPanel ?? true
        maxMemories.value = settings.maxMemories ?? 5
        
        if (enabled.value) {
          initializeMemOS()
        }
      }
    } catch (error) {
      console.error('Failed to load memory settings:', error)
    }
  }

  return {
    // State
    enabled,
    showPanel,
    maxMemories,
    memories,
    isLoading,
    error,
    
    // Computed
    hasMemories,
    recentMemories,
    
    // Actions
    initializeMemOS,
    searchMemories,
    storeMemory,
    updateMemory,
    deleteMemory,
    getContextMemories,
    clearMemories,
    toggleMemory,
    toggleMemoryPanel,
    setMaxMemories,
    saveSettings,
    loadSettings
  }
})
