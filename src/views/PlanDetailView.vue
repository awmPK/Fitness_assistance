<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <button
              @click="goBack"
              class="p-2 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors mr-4"
            >
              <i class="el-icon-arrow-left text-xl"></i>
            </button>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ plan?.name || '训练计划' }}</h1>
              <p class="text-sm text-gray-500">{{ plan?.description }}</p>
            </div>
          </div>
          <div class="flex space-x-3">
            <el-button @click="showEditDialog = true">
              <i class="el-icon-edit mr-2"></i>
              编辑
            </el-button>
            <el-button
              :type="plan?.status === 'active' ? 'danger' : 'success'"
              @click="togglePlanStatus"
            >
              <i :class="plan?.status === 'active' ? 'el-icon-video-pause' : 'el-icon-video-play'" class="mr-2"></i>
              {{ plan?.status === 'active' ? '暂停' : '继续' }}
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Plan Overview -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Progress Card -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900">训练进度</h2>
              <el-tag :type="getStatusType(plan?.status)" size="small">
                {{ getStatusText(plan?.status) }}
              </el-tag>
            </div>
            <div class="mb-4">
              <div class="flex justify-between text-sm text-gray-600 mb-2">
                <span>总体进度</span>
                <span>{{ Math.round(progressPercentage) }}%</span>
              </div>
              <el-progress :percentage="progressPercentage" :stroke-width="8"></el-progress>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="text-center">
                <div class="text-2xl font-bold text-primary-600">{{ completedWorkouts }}</div>
                <div class="text-sm text-gray-500">已完成</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-orange-600">{{ totalWorkouts }}</div>
                <div class="text-sm text-gray-500">总训练</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-green-600">{{ remainingDays }}</div>
                <div class="text-sm text-gray-500">剩余天数</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-purple-600">{{ streakDays }}</div>
                <div class="text-sm text-gray-500">连续天数</div>
              </div>
            </div>
          </div>

          <!-- Weekly Schedule -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900">本周训练安排</h2>
              <el-button size="small" @click="showAddWorkout = true">
                <i class="el-icon-plus mr-1"></i>
                添加训练
              </el-button>
            </div>
            <div class="space-y-3">
              <div
                v-for="day in weekDays"
                :key="day.date"
                class="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                :class="{ 'bg-primary-50 border-primary-200': day.hasWorkout }"
              >
                <div class="flex items-center">
                  <div class="w-10 h-10 rounded-full flex items-center justify-center"
                       :class="day.hasWorkout ? 'bg-primary-100 text-primary-600' : 'bg-gray-100 text-gray-500'">
                    <i :class="day.hasWorkout ? 'el-icon-sport' : 'el-icon-time'"></i>
                  </div>
                  <div class="ml-3">
                    <div class="font-medium text-gray-900">{{ day.name }}</div>
                    <div class="text-sm text-gray-500">{{ day.date }}</div>
                  </div>
                </div>
                <div class="text-right">
                  <div v-if="day.workout" class="text-sm font-medium text-gray-900">{{ day.workout.name }}</div>
                  <div v-if="day.workout" class="text-xs text-gray-500">{{ day.workout.duration }} 分钟</div>
                  <div v-else class="text-sm text-gray-400">休息日</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Workouts -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900">最近训练记录</h2>
              <el-button size="small" @click="showWorkoutHistory = true">
                查看全部
              </el-button>
            </div>
            <div v-if="recentWorkouts.length === 0" class="text-center py-8">
              <i class="el-icon-sport text-gray-300 text-4xl mb-3"></i>
              <p class="text-gray-500">还没有训练记录</p>
              <p class="text-sm text-gray-400 mt-1">完成您的第一次训练吧！</p>
            </div>
            <div v-else class="space-y-3">
              <div
                v-for="workout in recentWorkouts"
                :key="workout.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                    <i class="el-icon-sport text-primary-600"></i>
                  </div>
                  <div class="ml-3">
                    <div class="font-medium text-gray-900">{{ workout.type }}</div>
                    <div class="text-sm text-gray-500">{{ formatDate(workout.date) }}</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-sm font-medium text-gray-900">{{ workout.duration }} 分钟</div>
                  <div class="text-xs text-gray-500">{{ workout.calories }} 卡路里</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Plan Details -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">计划详情</h3>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">目标</span>
                <span class="font-medium">{{ getGoalText(plan?.goal) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">持续时间</span>
                <span class="font-medium">{{ plan?.duration }} 周</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">训练频率</span>
                <span class="font-medium">{{ plan?.frequency }} 次/周</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">开始日期</span>
                <span class="font-medium">{{ formatDate(plan?.startDate) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">结束日期</span>
                <span class="font-medium">{{ formatDate(plan?.endDate) }}</span>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">快速操作</h3>
            <div class="space-y-3">
              <button
                @click="startWorkout"
                class="w-full flex items-center justify-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                <i class="el-icon-video-play mr-2"></i>
                开始训练
              </button>
              <button
                @click="showAddWorkout = true"
                class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <i class="el-icon-plus mr-2"></i>
                添加训练
              </button>
              <button
                @click="showWorkoutHistory = true"
                class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <i class="el-icon-time mr-2"></i>
                历史记录
              </button>
              <button
                @click="showDeleteConfirm = true"
                class="w-full flex items-center justify-center px-4 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition-colors"
              >
                <i class="el-icon-delete mr-2"></i>
                删除计划
              </button>
            </div>
          </div>

          <!-- Statistics -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">统计数据</h3>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600">本周完成</span>
                  <span class="font-medium">{{ weeklyCompleted }}/{{ plan?.frequency }}</span>
                </div>
                <el-progress :percentage="weeklyProgress" :stroke-width="4"></el-progress>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600">本月完成</span>
                  <span class="font-medium">{{ monthlyCompleted }}</span>
                </div>
                <div class="text-2xl font-bold text-primary-600">{{ monthlyCompleted }}</div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600">总消耗</span>
                  <span class="font-medium">{{ totalCalories }} 卡路里</span>
                </div>
                <div class="text-2xl font-bold text-orange-600">{{ totalCalories }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Plan Dialog -->
    <el-dialog
      title="编辑计划"
      v-model="showEditDialog"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="100px">
        <el-form-item label="计划名称" prop="name">
          <el-input v-model="editForm.name" placeholder="输入计划名称"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="editForm.description"
            type="textarea"
            :rows="3"
            placeholder="描述您的训练目标..."
          ></el-input>
        </el-form-item>
        <el-form-item label="目标" prop="goal">
          <el-select v-model="editForm.goal" placeholder="选择训练目标" style="width: 100%">
            <el-option label="减脂" value="weight_loss"></el-option>
            <el-option label="增肌" value="muscle_gain"></el-option>
            <el-option label="塑形" value="body_shaping"></el-option>
            <el-option label="力量" value="strength"></el-option>
            <el-option label="耐力" value="endurance"></el-option>
            <el-option label="综合" value="general"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="持续时间" prop="duration">
          <el-input-number
            v-model="editForm.duration"
            :min="1"
            :max="52"
            placeholder="周数"
          ></el-input-number>
          <span class="ml-2 text-gray-500">周</span>
        </el-form-item>
        <el-form-item label="训练频率" prop="frequency">
          <el-input-number
            v-model="editForm.frequency"
            :min="1"
            :max="7"
            placeholder="次数"
          ></el-input-number>
          <span class="ml-2 text-gray-500">次/周</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="submitEdit" :loading="submitting">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Add Workout Dialog -->
    <el-dialog
      title="添加训练"
      v-model="showAddWorkout"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="workoutForm" :rules="workoutRules" ref="workoutFormRef" label-width="80px">
        <el-form-item label="训练名称" prop="name">
          <el-input v-model="workoutForm.name" placeholder="输入训练名称"></el-input>
        </el-form-item>
        <el-form-item label="日期" prop="date">
          <el-date-picker
            v-model="workoutForm.date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="时长" prop="duration">
          <el-input-number
            v-model="workoutForm.duration"
            :min="5"
            :max="300"
            placeholder="分钟"
          ></el-input-number>
          <span class="ml-2 text-gray-500">分钟</span>
        </el-form-item>
        <el-form-item label="卡路里" prop="calories">
          <el-input-number
            v-model="workoutForm.calories"
            :min="0"
            :max="2000"
            placeholder="卡路里"
          ></el-input-number>
          <span class="ml-2 text-gray-500">卡路里</span>
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="workoutForm.notes"
            type="textarea"
            :rows="3"
            placeholder="训练备注..."
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddWorkout = false">取消</el-button>
          <el-button type="primary" @click="submitWorkout" :loading="submitting">
            添加
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Delete Confirmation -->
    <el-dialog
      title="删除计划"
      v-model="showDeleteConfirm"
      width="400px"
    >
      <div class="text-center py-4">
        <i class="el-icon-warning text-red-500 text-4xl mb-3"></i>
        <p class="text-gray-900 mb-2">确定要删除这个训练计划吗？</p>
        <p class="text-sm text-gray-500">此操作无法撤销，所有相关数据将被删除。</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDeleteConfirm = false">取消</el-button>
          <el-button type="danger" @click="deletePlan" :loading="submitting">
            删除
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useFitnessStore } from '@/stores/fitness'
import { useUserStore } from '@/stores/user'
import type { FitnessPlan, Workout } from '@/types'

const route = useRoute()
const router = useRouter()
const fitnessStore = useFitnessStore()
const userStore = useUserStore()

// State
const plan = ref<FitnessPlan | null>(null)
const loading = ref(false)
const showEditDialog = ref(false)
const showAddWorkout = ref(false)
const showWorkoutHistory = ref(false)
const showDeleteConfirm = ref(false)
const submitting = ref(false)

// Forms
const editFormRef = ref()
const workoutFormRef = ref()

const editForm = reactive({
  name: '',
  description: '',
  goal: 'general',
  duration: 4,
  frequency: 3
})

const editRules = {
  name: [
    { required: true, message: '请输入计划名称', trigger: 'blur' },
    { min: 2, max: 50, message: '名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入计划描述', trigger: 'blur' },
    { min: 10, max: 500, message: '描述长度在 10 到 500 个字符', trigger: 'blur' }
  ],
  goal: [{ required: true, message: '请选择训练目标', trigger: 'change' }],
  duration: [{ required: true, message: '请输入持续时间', trigger: 'blur' }],
  frequency: [{ required: true, message: '请输入训练频率', trigger: 'blur' }]
}

const workoutForm = reactive({
  name: '',
  date: new Date(),
  duration: 30,
  calories: 200,
  notes: ''
})

const workoutRules = {
  name: [
    { required: true, message: '请输入训练名称', trigger: 'blur' },
    { min: 2, max: 50, message: '名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  duration: [{ required: true, message: '请输入时长', trigger: 'blur' }],
  calories: [{ required: true, message: '请输入卡路里', trigger: 'blur' }]
}

// Computed
const progressPercentage = computed(() => {
  if (!plan.value) return 0
  const start = new Date(plan.value.startDate).getTime()
  const end = new Date(plan.value.endDate).getTime()
  const now = Date.now()
  
  if (now >= end) return 100
  if (now <= start) return 0
  
  const total = end - start
  const elapsed = now - start
  return Math.round((elapsed / total) * 100)
})

const completedWorkouts = computed(() => {
  return plan.value?.workouts?.filter(w => w.completed).length || 0
})

const totalWorkouts = computed(() => {
  return plan.value?.workouts?.length || 0
})

const remainingDays = computed(() => {
  if (!plan.value) return 0
  const end = new Date(plan.value.endDate)
  const now = new Date()
  const diffTime = end.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return Math.max(0, diffDays)
})

const streakDays = computed(() => {
  // Calculate current workout streak
  return fitnessStore.currentStreak
})

const recentWorkouts = computed(() => {
  const workouts = plan.value?.workouts || []
  return workouts
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .slice(0, 5)
})

const weeklyCompleted = computed(() => {
  // Calculate workouts completed this week
  const now = new Date()
  const startOfWeek = new Date(now.setDate(now.getDate() - now.getDay()))
  return plan.value?.workouts?.filter(w => {
    const workoutDate = new Date(w.date)
    return workoutDate >= startOfWeek && w.completed
  }).length || 0
})

const weeklyProgress = computed(() => {
  if (!plan.value) return 0
  return Math.round((weeklyCompleted.value / plan.value.frequency) * 100)
})

const monthlyCompleted = computed(() => {
  // Calculate workouts completed this month
  const now = new Date()
  const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
  return plan.value?.workouts?.filter(w => {
    const workoutDate = new Date(w.date)
    return workoutDate >= startOfMonth && w.completed
  }).length || 0
})

const totalCalories = computed(() => {
  return plan.value?.workouts?.reduce((total, w) => total + (w.calories || 0), 0) || 0
})

const weekDays = computed(() => {
  const days = []
  const today = new Date()
  const startOfWeek = new Date(today.setDate(today.getDate() - today.getDay()))
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(startOfWeek)
    date.setDate(startOfWeek.getDate() + i)
    
    const dayWorkouts = plan.value?.workouts?.filter(w => {
      const workoutDate = new Date(w.date)
      return workoutDate.toDateString() === date.toDateString()
    }) || []
    
    days.push({
      name: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][i],
      date: date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }),
      hasWorkout: dayWorkouts.length > 0,
      workout: dayWorkouts[0],
      completed: dayWorkouts.some(w => w.completed)
    })
  }
  
  return days
})

// Methods
const goBack = () => {
  router.push('/plans')
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'active': return 'success'
    case 'completed': return 'info'
    case 'paused': return 'warning'
    default: return 'info'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'active': return '进行中'
    case 'completed': return '已完成'
    case 'paused': return '暂停'
    default: return '未知'
  }
}

const getGoalText = (goal: string) => {
  switch (goal) {
    case 'weight_loss': return '减脂'
    case 'muscle_gain': return '增肌'
    case 'body_shaping': return '塑形'
    case 'strength': return '力量'
    case 'endurance': return '耐力'
    case 'general': return '综合'
    default: return goal
  }
}

const formatDate = (date: Date | string | undefined) => {
  if (!date) return '未知'
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN')
}

const togglePlanStatus = async () => {
  if (!plan.value) return
  
  const newStatus = plan.value.status === 'active' ? 'paused' : 'active'
  
  try {
    await fitnessStore.updatePlan(plan.value.id, { status: newStatus })
    plan.value.status = newStatus
    ElMessage.success(newStatus === 'active' ? '计划已继续' : '计划已暂停')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const startWorkout = () => {
  ElMessage.info('开始训练功能开发中...')
}

const submitEdit = async () => {
  if (!editFormRef.value || !plan.value) return
  
  try {
    await editFormRef.value.validate()
    submitting.value = true
    
    await fitnessStore.updatePlan(plan.value.id, editForm)
    
    // Update local plan
    Object.assign(plan.value, editForm)
    
    ElMessage.success('计划更新成功')
    showEditDialog.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('更新计划失败')
    }
  } finally {
    submitting.value = false
  }
}

const submitWorkout = async () => {
  if (!workoutFormRef.value || !plan.value) return
  
  try {
    await workoutFormRef.value.validate()
    submitting.value = true
    
    const workout = await fitnessStore.addWorkout(plan.value.id, workoutForm)
    
    // Add to plan workouts
    if (!plan.value.workouts) {
      plan.value.workouts = []
    }
    plan.value.workouts.push(workout)
    
    ElMessage.success('训练添加成功')
    showAddWorkout.value = false
    
    // Reset form
    Object.assign(workoutForm, {
      name: '',
      date: new Date(),
      duration: 30,
      calories: 200,
      notes: ''
    })
  } catch (error) {
    if (error !== false) {
      ElMessage.error('添加训练失败')
    }
  } finally {
    submitting.value = false
  }
}

const deletePlan = async () => {
  if (!plan.value) return
  
  try {
    submitting.value = true
    await fitnessStore.deletePlan(plan.value.id)
    ElMessage.success('计划删除成功')
    router.push('/plans')
  } catch (error) {
    ElMessage.error('删除计划失败')
  } finally {
    submitting.value = false
    showDeleteConfirm.value = false
  }
}

// Load plan data
const loadPlan = async () => {
  const planId = route.params.id as string
  if (!planId) {
    router.push('/plans')
    return
  }
  
  loading.value = true
  try {
    const planData = await fitnessStore.getPlan(planId)
    if (!planData) {
      ElMessage.error('计划不存在')
      router.push('/plans')
      return
    }
    
    plan.value = planData
    
    // Initialize edit form
    Object.assign(editForm, {
      name: planData.name,
      description: planData.description,
      goal: planData.goal,
      duration: planData.duration,
      frequency: planData.frequency
    })
  } catch (error) {
    ElMessage.error('加载计划失败')
    router.push('/plans')
  } finally {
    loading.value = false
  }
}

// Load data on mount
onMounted(() => {
  loadPlan()
})
</script>

<style scoped>
.el-progress-bar__outer {
  background-color: #f3f4f6;
}
</style>
