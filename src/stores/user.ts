import { defineStore } from 'pinia'
import { ref } from 'vue'
import { userApi } from '@/services/api'
import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)

  const loadUser = async () => {
    // 使用 JWT token 获取当前用户信息
    const token = localStorage.getItem('token')
    if (!token) {
      user.value = null
      return
    }
    
    try {
      const res = await userApi.getCurrentUser()
      if (res.success) {
        user.value = res.data as unknown as User
        localStorage.setItem('user_id', user.value.user_id)
      }
    } catch (error) {
      // Token 无效，清除登录状态
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      user.value = null
    }
  }

  const loadUserProfile = loadUser

  const updateProfile = async (data: Partial<User>) => {
    if (!user.value) return
    const res = await userApi.updateUser(user.value.user_id, data)
    if (res.success) {
      user.value = res.data as unknown as User
    }
  }

  const updateHealthData = async (data: Record<string, any>) => {
    if (!user.value) return
    const res = await userApi.updateUser(user.value.user_id, data)
    if (res.success) {
      user.value = { ...user.value!, ...(res.data as any) }
    }
  }

  const login = async (payload: { email: string; password: string }) => {
    const res = await userApi.login(payload.email, payload.password)
    if (res.success) {
      const { user: u, token } = res.data as any
      localStorage.setItem('token', token)
      localStorage.setItem('user_id', u.user_id)
      user.value = u
    } else {
      throw new Error(res.message || '登录失败')
    }
  }

  const register = async (data: { email: string; password: string; name: string }) => {
    const res = await userApi.register(data)
    if (res.success) {
      const { user: u, token } = res.data as any
      localStorage.setItem('token', token)
      localStorage.setItem('user_id', u.user_id)
      user.value = u
    } else {
      throw new Error(res.message || '注册失败')
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('current_conversation_id')
    user.value = null
  }

  return {
    user,
    loadUser,
    loadUserProfile,
    updateProfile,
    updateHealthData,
    login,
    register,
    logout,
  }
})
