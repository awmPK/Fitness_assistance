import axios from 'axios'
import type { 
  ChatRequest, 
  ChatResponse, 
  ApiResponse, 
  User, 
  Conversation,
  Memory 
} from '@/types'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Chat API
export const chatApi = {
  sendMessage: async (data: ChatRequest): Promise<ApiResponse<ChatResponse>> => {
    const response = await api.post('/chat/send', data)
    return response.data
  },

  getConversationHistory: async (conversationId: string): Promise<ApiResponse<Conversation>> => {
    const response = await api.get(`/chat/conversation/${conversationId}`)
    return response.data
  },

  getConversations: async (userId: string): Promise<ApiResponse<Conversation[]>> => {
    const response = await api.get(`/chat/conversations/${userId}`)
    return response.data
  }
}

// User API
export const userApi = {
  getUser: async (userId: string): Promise<ApiResponse<User>> => {
    const response = await api.get(`/user/${userId}`)
    return response.data
  },

  updateUser: async (userId: string, data: Partial<User>): Promise<ApiResponse<User>> => {
    const response = await api.put(`/user/${userId}`, data)
    return response.data
  },

  login: async (email: string, password: string): Promise<ApiResponse<{ user: User; token: string }>> => {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  register: async (data: { email: string; password: string; name: string }): Promise<ApiResponse<{ user: User; token: string }>> => {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    const response = await api.get('/auth/me')
    return response.data
  },

  changePassword: async (userId: string, currentPassword: string, newPassword: string): Promise<ApiResponse<null>> => {
    const response = await api.put(`/user/${userId}/password`, {
      current_password: currentPassword,
      new_password: newPassword
    })
    return response.data
  }
}

// MemOS API (for memory operations)
export const memosApi = {
  searchMemory: async (query: string, userId: string, conversationId?: string): Promise<ApiResponse<Memory[]>> => {
    const response = await api.post('/memos/search', { query, userId, conversationId })
    return response.data
  },

  addMessage: async (messages: Array<{ role: string; content: string }>, userId: string, conversationId: string): Promise<ApiResponse<void>> => {
    const response = await api.post('/memos/messages', { messages, userId, conversationId })
    return response.data
  },

  getMemoryStats: async (userId: string): Promise<ApiResponse<{ total_memories: number; recent_memories: number }>> => {
    const response = await api.get(`/memos/stats/${userId}`)
    return response.data
  }
}

export default api
