import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { FitnessPlan } from '@/types'

export const useFitnessStore = defineStore('fitness', () => {
  const plans = ref<FitnessPlan[]>([])
  const activities = ref<Array<{ id: string; type: string; date: string; duration: number; calories: number }>>([])
  const achievements = ref<Array<{ id: string; name: string; icon: string; earned: boolean }>>([])
  const currentStreak = ref(0)

  const loadPlans = async () => {
    // Placeholder: load from server later
    plans.value = []
  }

  const createPlan = async (data: any) => {
    const id = `plan_${Date.now()}`
    plans.value.push({
      id,
      userId: data.userId,
      name: data.name,
      description: data.description,
      goal: data.goal,
      duration: data.duration,
      frequency: data.frequency,
      startDate: data.startDate,
      endDate: data.endDate,
      status: 'active',
    })
  }

  const updatePlan = async (id: string, patch: Partial<FitnessPlan>) => {
    plans.value = plans.value.map(p => p.id === id ? { ...p, ...patch } : p)
  }

  const getPlan = async (id: string) => {
    return plans.value.find(p => p.id === id) || null
  }

  const addWorkout = async (planId: string, workout: any) => {
    const plan = plans.value.find(p => p.id === planId)
    if (!plan) return null
    const w = { id: `w_${Date.now()}`, completed: false, ...workout }
    plan.workouts = plan.workouts || []
    plan.workouts.push(w)
    return w
  }

  const deletePlan = async (id: string) => {
    plans.value = plans.value.filter(p => p.id !== id)
  }

  const loadActivities = async () => {
    activities.value = []
  }

  const loadAchievements = async () => {
    achievements.value = [
      { id: 'a1', name: '首次训练', icon: 'el-icon-medal', earned: true },
      { id: 'a2', name: '连练7天', icon: 'el-icon-star-on', earned: false },
    ]
  }

  return {
    plans,
    activities,
    achievements,
    currentStreak,
    loadPlans,
    createPlan,
    updatePlan,
    getPlan,
    addWorkout,
    deletePlan,
    loadActivities,
    loadAchievements,
  }
})
