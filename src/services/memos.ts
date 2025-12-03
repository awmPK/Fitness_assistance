import axios from 'axios'
import type { AxiosInstance } from 'axios'
import type { Memory, MemoryQuery, CreateMemoryRequest, UpdateMemoryRequest } from '@/types'

export interface MemOSConfig {
  apiKey: string
  baseURL: string
  timeout?: number
}

export class MemOSClient {
  private client: AxiosInstance
  private config: MemOSConfig

  constructor(config: MemOSConfig) {
    this.config = config
    
    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout || 30000,
      headers: {
        'Authorization': `Bearer ${config.apiKey}`,
        'Content-Type': 'application/json'
      }
    })

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          console.error('MemOS authentication failed')
        }
        return Promise.reject(error)
      }
    )
  }

  /**
   * Search memories by query
   */
  async search(query: MemoryQuery): Promise<Memory[]> {
    try {
      const response = await this.client.post('/api/v1/memories/search', {
        query: query.query,
        limit: query.limit || 10,
        threshold: query.threshold || 0.7,
        filters: query.filters || {},
        user_id: query.userId
      })
      
      return response.data.memories || []
    } catch (error) {
      console.error('Failed to search memories:', error)
      throw new Error('搜索记忆失败')
    }
  }

  /**
   * Store a new memory
   */
  async store(content: string, metadata?: Record<string, any>): Promise<Memory> {
    try {
      const request: CreateMemoryRequest = {
        content,
        metadata: metadata || {},
        type: 'text',
        timestamp: new Date().toISOString()
      }
      
      const response = await this.client.post('/api/v1/memories', request)
      return response.data.memory
    } catch (error) {
      console.error('Failed to store memory:', error)
      throw new Error('存储记忆失败')
    }
  }

  /**
   * Get memory by ID
   */
  async get(id: string): Promise<Memory | null> {
    try {
      const response = await this.client.get(`/api/v1/memories/${id}`)
      return response.data.memory
    } catch (error) {
      if (error.response?.status === 404) {
        return null
      }
      console.error('Failed to get memory:', error)
      throw new Error('获取记忆失败')
    }
  }

  /**
   * Update memory
   */
  async update(id: string, content: string, metadata?: Record<string, any>): Promise<Memory> {
    try {
      const request: UpdateMemoryRequest = {
        content,
        metadata: metadata || {},
        timestamp: new Date().toISOString()
      }
      
      const response = await this.client.put(`/api/v1/memories/${id}`, request)
      return response.data.memory
    } catch (error) {
      console.error('Failed to update memory:', error)
      throw new Error('更新记忆失败')
    }
  }

  /**
   * Delete memory
   */
  async delete(id: string): Promise<boolean> {
    try {
      await this.client.delete(`/api/v1/memories/${id}`)
      return true
    } catch (error) {
      console.error('Failed to delete memory:', error)
      throw new Error('删除记忆失败')
    }
  }

  /**
   * Get recent memories
   */
  async getRecent(limit = 10, userId?: string): Promise<Memory[]> {
    try {
      const response = await this.client.get('/api/v1/memories/recent', {
        params: { limit, user_id: userId }
      })
      return response.data.memories || []
    } catch (error) {
      console.error('Failed to get recent memories:', error)
      throw new Error('获取最近记忆失败')
    }
  }

  /**
   * Get memories by type
   */
  async getByType(type: string, limit = 10, userId?: string): Promise<Memory[]> {
    try {
      const response = await this.client.get('/api/v1/memories/type', {
        params: { type, limit, user_id: userId }
      })
      return response.data.memories || []
    } catch (error) {
      console.error('Failed to get memories by type:', error)
      throw new Error('获取类型记忆失败')
    }
  }

  /**
   * Batch store memories
   */
  async batchStore(memories: CreateMemoryRequest[]): Promise<Memory[]> {
    try {
      const response = await this.client.post('/api/v1/memories/batch', {
        memories
      })
      return response.data.memories || []
    } catch (error) {
      console.error('Failed to batch store memories:', error)
      throw new Error('批量存储记忆失败')
    }
  }

  /**
   * Get memory statistics
   */
  async getStats(userId?: string): Promise<{
    total: number
    byType: Record<string, number>
    recentCount: number
  }> {
    try {
      const response = await this.client.get('/api/v1/memories/stats', {
        params: { user_id: userId }
      })
      return response.data.stats
    } catch (error) {
      console.error('Failed to get memory stats:', error)
      throw new Error('获取记忆统计失败')
    }
  }

  /**
   * Clear all memories for a user
   */
  async clearAll(userId?: string): Promise<boolean> {
    try {
      await this.client.delete('/api/v1/memories', {
        params: { user_id: userId }
      })
      return true
    } catch (error) {
      console.error('Failed to clear memories:', error)
      throw new Error('清空记忆失败')
    }
  }
}

// Export singleton instance
let memosClient: MemOSClient | null = null

export const getMemOSClient = (config?: MemOSConfig): MemOSClient => {
  if (!memosClient && config) {
    memosClient = new MemOSClient(config)
  }
  
  if (!memosClient) {
    throw new Error('MemOS client not initialized')
  }
  
  return memosClient
}

export const initializeMemOS = (config: MemOSConfig) => {
  memosClient = new MemOSClient(config)
  return memosClient
}
