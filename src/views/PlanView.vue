<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <div class="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg">
              <i class="el-icon-document text-primary-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h1 class="text-2xl font-bold text-gray-900">健身计划</h1>
              <p class="text-sm text-gray-500">管理您的训练计划和进度</p>
            </div>
          </div>
          <el-button type="primary" @click="showCreatePlanDialog = true">
            <i class="el-icon-plus mr-2"></i>
            创建计划
          </el-button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-blue-100 rounded-lg p-3">
              <i class="el-icon-trophy text-blue-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">总计划数</p>
              <p class="text-2xl font-bold text-gray-900">{{ fitnessStore.plans.length }}</p>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-green-100 rounded-lg p-3">
              <i class="el-icon-check text-green-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">已完成</p>
              <p class="text-2xl font-bold text-gray-900">{{ completedPlansCount }}</p>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-orange-100 rounded-lg p-3">
              <i class="el-icon-time text-orange-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">进行中</p>
              <p class="text-2xl font-bold text-gray-900">{{ activePlansCount }}</p>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-purple-100 rounded-lg p-3">
              <i class="el-icon-star text-purple-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">本周训练</p>
              <p class="text-2xl font-bold text-gray-900">{{ weeklyWorkouts }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Plans List -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">训练计划</h2>
            <div class="flex items-center space-x-4">
              <el-select v-model="filterStatus" placeholder="筛选状态" size="small" style="width: 120px">
                <el-option label="全部" value=""></el-option>
                <el-option label="进行中" value="active"></el-option>
                <el-option label="已完成" value="completed"></el-option>
                <el-option label="暂停" value="paused"></el-option>
              </el-select>
              <el-input
                v-model="searchQuery"
                placeholder="搜索计划..."
                size="small"
                style="width: 200px"
                clearable
              >
                <template #prefix>
                  <i class="el-icon-search"></i>
                </template>
              </el-input>
            </div>
          </div>
        </div>

        <div class="p-6">
          <div v-if="filteredPlans.length === 0" class="text-center py-12">
            <i class="el-icon-document text-gray-300 text-6xl mb-4"></i>
            <h3 class="text-lg font-medium text-gray-900 mb-2">还没有训练计划</h3>
            <p class="text-gray-500 mb-4">创建您的第一个健身计划开始训练吧！</p>
            <el-button type="primary" @click="showCreatePlanDialog = true">
              <i class="el-icon-plus mr-2"></i>
              创建计划
            </el-button>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4 md:gap-6 plan-grid">
            <div
              v-for="plan in filteredPlans"
              :key="plan.id"
              class="bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow duration-200"
            >
              <div class="p-6">
                <div class="flex items-start justify-between mb-4">
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ plan.name }}</h3>
                    <p class="text-sm text-gray-500">{{ plan.description }}</p>
                  </div>
                  <el-tag :type="getStatusType(plan.status)" size="small">
                    {{ getStatusText(plan.status) }}
                  </el-tag>
                </div>

                <div class="space-y-3 mb-4">
                  <div class="flex items-center text-sm text-gray-600">
                    <i class="el-icon-calendar mr-2"></i>
                    <span>{{ formatDate(plan.startDate) }} - {{ formatDate(plan.endDate) }}</span>
                  </div>
                  <div class="flex items-center text-sm text-gray-600">
                    <i class="el-icon-time mr-2"></i>
                    <span>{{ plan.duration }} 周 · {{ plan.frequency }} 次/周</span>
                  </div>
                  <div class="flex items-center text-sm text-gray-600">
                    <i class="el-icon-target mr-2"></i>
                    <span>{{ plan.goal }}</span>
                  </div>
                </div>

                <!-- Progress Bar -->
                <div class="mb-4">
                  <div class="flex justify-between text-sm text-gray-600 mb-1">
                    <span>进度</span>
                    <span>{{ Math.round(calculateProgress(plan)) }}%</span>
                  </div>
                  <el-progress :percentage="calculateProgress(plan)" :stroke-width="6"></el-progress>
                </div>

                <!-- Action Buttons -->
                <div class="flex space-x-2">
                  <el-button type="primary" size="small" @click="viewPlan(plan)">
                    <i class="el-icon-view mr-1"></i>
                    查看
                  </el-button>
                  <el-button size="small" @click="editPlan(plan)">
                    <i class="el-icon-edit mr-1"></i>
                    编辑
                  </el-button>
                  <el-button
                    v-if="plan.status === 'active'"
                    type="danger"
                    size="small"
                    @click="pausePlan(plan)"
                  >
                    <i class="el-icon-video-pause mr-1"></i>
                    暂停
                  </el-button>
                  <el-button
                    v-else
                    type="success"
                    size="small"
                    @click="resumePlan(plan)"
                  >
                    <i class="el-icon-video-play mr-1"></i>
                    继续
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Plan Dialog -->
    <el-dialog
      :title="editingPlan ? '编辑计划' : '创建计划'"
      v-model="showCreatePlanDialog"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="planForm" :rules="planRules" ref="planFormRef" label-width="100px">
        <el-form-item label="计划名称" prop="name">
          <el-input v-model="planForm.name" placeholder="输入计划名称"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="planForm.description"
            type="textarea"
            :rows="3"
            placeholder="描述您的训练目标..."
          ></el-input>
        </el-form-item>
        <el-form-item label="目标" prop="goal">
          <el-select v-model="planForm.goal" placeholder="选择训练目标" style="width: 100%">
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
            v-model="planForm.duration"
            :min="1"
            :max="52"
            placeholder="周数"
          ></el-input-number>
          <span class="ml-2 text-gray-500">周</span>
        </el-form-item>
        <el-form-item label="训练频率" prop="frequency">
          <el-input-number
            v-model="planForm.frequency"
            :min="1"
            :max="7"
            placeholder="次数"
          ></el-input-number>
          <span class="ml-2 text-gray-500">次/周</span>
        </el-form-item>
        <el-form-item label="开始日期" prop="startDate">
          <el-date-picker
            v-model="planForm.startDate"
            type="date"
            placeholder="选择开始日期"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="结束日期" prop="endDate">
          <el-date-picker
            v-model="planForm.endDate"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreatePlanDialog = false">取消</el-button>
          <el-button type="primary" @click="submitPlan" :loading="submitting">
            {{ editingPlan ? '更新' : '创建' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useFitnessStore } from '@/stores/fitness'
import { useUserStore } from '@/stores/user'
import type { FitnessPlan, CreatePlanRequest } from '@/types'

const router = useRouter()
const fitnessStore = useFitnessStore()
const userStore = useUserStore()

// State
const filterStatus = ref('')
const searchQuery = ref('')
const showCreatePlanDialog = ref(false)
const editingPlan = ref<FitnessPlan | null>(null)
const submitting = ref(false)

// Form
const planFormRef = ref()
const planForm = reactive<CreatePlanRequest>({
  name: '',
  description: '',
  goal: 'general',
  duration: 4,
  frequency: 3,
  startDate: new Date(),
  endDate: new Date(Date.now() + 28 * 24 * 60 * 60 * 1000), // 4 weeks from now
  userId: ''
})

const planRules = {
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
  frequency: [{ required: true, message: '请输入训练频率', trigger: 'blur' }],
  startDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  endDate: [{ required: true, message: '请选择结束日期', trigger: 'change' }]
}

// Computed
const filteredPlans = computed(() => {
  let plans = fitnessStore.plans

  if (filterStatus.value) {
    plans = plans.filter(plan => plan.status === filterStatus.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    plans = plans.filter(plan => 
      plan.name.toLowerCase().includes(query) ||
      plan.description.toLowerCase().includes(query) ||
      plan.goal.toLowerCase().includes(query)
    )
  }

  return plans
})

const completedPlansCount = computed(() => 
  fitnessStore.plans.filter(plan => plan.status === 'completed').length
)

const activePlansCount = computed(() => 
  fitnessStore.plans.filter(plan => plan.status === 'active').length
)

const weeklyWorkouts = computed(() => {
  // Calculate workouts completed this week
  return fitnessStore.plans.reduce((total, plan) => {
    if (plan.status === 'active') {
      return total + (plan.frequency || 0)
    }
    return total
  }, 0)
})

// Methods
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

const formatDate = (date: Date | string) => {
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN')
}

const calculateProgress = (plan: FitnessPlan) => {
  const start = new Date(plan.startDate).getTime()
  const end = new Date(plan.endDate).getTime()
  const now = Date.now()
  
  if (now >= end) return 100
  if (now <= start) return 0
  
  const total = end - start
  const elapsed = now - start
  return Math.round((elapsed / total) * 100)
}

const viewPlan = (plan: FitnessPlan) => {
  router.push(`/plans/${plan.id}`)
}

const editPlan = (plan: FitnessPlan) => {
  editingPlan.value = plan
  Object.assign(planForm, {
    name: plan.name,
    description: plan.description,
    goal: plan.goal,
    duration: plan.duration,
    frequency: plan.frequency,
    startDate: new Date(plan.startDate),
    endDate: new Date(plan.endDate)
  })
  showCreatePlanDialog.value = true
}

const pausePlan = async (plan: FitnessPlan) => {
  try {
    await fitnessStore.updatePlan(plan.id, { status: 'paused' })
    ElMessage.success('计划已暂停')
  } catch (error) {
    ElMessage.error('暂停计划失败')
  }
}

const resumePlan = async (plan: FitnessPlan) => {
  try {
    await fitnessStore.updatePlan(plan.id, { status: 'active' })
    ElMessage.success('计划已继续')
  } catch (error) {
    ElMessage.error('继续计划失败')
  }
}

const submitPlan = async () => {
  if (!planFormRef.value) return
  
  try {
    await planFormRef.value.validate()
    submitting.value = true
    
    const userId = userStore.user?.user_id
    if (!userId) {
      ElMessage.error('用户未登录')
      return
    }
    
    const planData = {
      ...planForm,
      userId,
      startDate: planForm.startDate.toISOString(),
      endDate: planForm.endDate.toISOString()
    }
    
    if (editingPlan.value) {
      await fitnessStore.updatePlan(editingPlan.value.id, planData)
      ElMessage.success('计划更新成功')
    } else {
      await fitnessStore.createPlan(planData)
      ElMessage.success('计划创建成功')
    }
    
    showCreatePlanDialog.value = false
    resetForm()
  } catch (error) {
    if (error !== false) {
      ElMessage.error(editingPlan.value ? '更新计划失败' : '创建计划失败')
    }
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  editingPlan.value = null
  Object.assign(planForm, {
    name: '',
    description: '',
    goal: 'general',
    duration: 4,
    frequency: 3,
    startDate: new Date(),
    endDate: new Date(Date.now() + 28 * 24 * 60 * 60 * 1000),
    userId: ''
  })
}

// Watch for dialog close
watch(showCreatePlanDialog, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})

// Load plans on mount
onMounted(async () => {
  try {
    await fitnessStore.loadPlans()
  } catch (error) {
    ElMessage.error('加载计划失败')
  }
})
</script>

<style scoped>
.el-progress-bar__outer {
  background-color: #f3f4f6;
}
</style>
