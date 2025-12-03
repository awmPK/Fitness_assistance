import { defineStore } from 'pinia'
import { ref } from 'vue'
import { userApi } from '@/services/api'
import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)

  const loadUser = async () => {
    const uid = localStorage.getItem('user_id') || 'fitness_user_123'
    const res = await userApi.getUser(uid)
    if (res.success) {
      user.value = res.data as unknown as User
      localStorage.setItem('user_id', user.value.user_id)
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
      user.value = u
      localStorage.setItem('user_id', u.user_id)
    }
  }

  const register = async (data: { email: string; password: string; name: string }) => {
    const res = await userApi.register(data)
    if (res.success) {
      const { user: u, token } = res.data as any
      localStorage.setItem('token', token)
      user.value = u
      localStorage.setItem('user_id', u.user_id)
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
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
