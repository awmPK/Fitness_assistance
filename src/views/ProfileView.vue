<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <div class="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg">
              <i class="el-icon-user text-primary-600 text-xl"></i>
            </div>
            <div class="ml-4">
              <h1 class="text-2xl font-bold text-gray-900">个人中心</h1>
              <p class="text-sm text-gray-500">管理您的个人信息和健身数据</p>
            </div>
          </div>
          <el-button type="primary" @click="showEditProfile = true">
            <i class="el-icon-edit mr-2"></i>
            编辑资料
          </el-button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Profile Card -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="text-center mb-6">
              <div class="relative inline-block">
                <img
                  :src="userStore.user?.avatar || 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Fitness%20avatar%20icon%20with%20dumbbell%20and%20muscle%20silhouette%20on%20white%20background%20clean%20minimalist%20design&image_size=square'"
                  :alt="userStore.user?.name || '用户头像'"
                  class="w-24 h-24 rounded-full object-cover border-4 border-primary-100"
                />
                <button
                  @click="showAvatarUpload = true"
                  class="absolute bottom-0 right-0 bg-primary-600 text-white rounded-full p-2 hover:bg-primary-700 transition-colors"
                >
                  <i class="el-icon-camera text-sm"></i>
                </button>
              </div>
              <h2 class="text-xl font-semibold text-gray-900 mt-4">{{ userStore.user?.name || '健身达人' }}</h2>
              <p class="text-gray-500">{{ userStore.user?.email || 'user@example.com' }}</p>
              <div class="flex items-center justify-center mt-2">
                <el-tag :type="getLevelType(userStore.user?.fitnessLevel)" size="small">
                  {{ getLevelText(userStore.user?.fitnessLevel) }}
                </el-tag>
              </div>
            </div>

            <div class="space-y-4">
              <div class="flex justify-between items-center py-2 border-b border-gray-100">
                <span class="text-gray-600">注册时间</span>
                <span class="text-gray-900">{{ formatDate(userStore.user?.createdAt) }}</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b border-gray-100">
                <span class="text-gray-600">最后登录</span>
                <span class="text-gray-900">{{ formatDate(userStore.user?.lastLoginAt) }}</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b border-gray-100">
                <span class="text-gray-600">身高</span>
                <span class="text-gray-900">{{ userStore.user?.height || '未设置' }} cm</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b border-gray-100">
                <span class="text-gray-600">体重</span>
                <span class="text-gray-900">{{ userStore.user?.weight || '未设置' }} kg</span>
              </div>
              <div class="flex justify-between items-center py-2">
                <span class="text-gray-600">年龄</span>
                <span class="text-gray-900">{{ userStore.user?.age || '未设置' }} 岁</span>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mt-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">快速操作</h3>
            <div class="space-y-3">
              <button
                @click="showEditProfile = true"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg transition-colors"
              >
                <div class="flex items-center">
                  <i class="el-icon-edit text-primary-600 mr-3"></i>
                  <span class="text-gray-900">编辑个人资料</span>
                </div>
                <i class="el-icon-arrow-right text-gray-400"></i>
              </button>
              <button
                @click="showHealthForm = true"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg transition-colors"
              >
                <div class="flex items-center">
                  <i class="el-icon-medal text-primary-600 mr-3"></i>
                  <span class="text-gray-900">更新健康数据</span>
                </div>
                <i class="el-icon-arrow-right text-gray-400"></i>
              </button>
              <button
                @click="showSettings = true"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg transition-colors"
              >
                <div class="flex items-center">
                  <i class="el-icon-setting text-primary-600 mr-3"></i>
                  <span class="text-gray-900">应用设置</span>
                </div>
                <i class="el-icon-arrow-right text-gray-400"></i>
              </button>
              <button
                @click="showPrivacySettings = true"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg transition-colors"
              >
                <div class="flex items-center">
                  <i class="el-icon-lock text-primary-600 mr-3"></i>
                  <span class="text-gray-900">隐私设置</span>
                </div>
                <i class="el-icon-arrow-right text-gray-400"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Stats and Activity -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Stats Overview -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 profile-stats">
            <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200 text-center">
              <div class="text-2xl font-bold text-primary-600">{{ totalWorkouts }}</div>
              <div class="text-sm text-gray-500">总训练次数</div>
            </div>
            <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200 text-center">
              <div class="text-2xl font-bold text-green-600">{{ totalDuration }}</div>
              <div class="text-sm text-gray-500">总训练时长(分钟)</div>
            </div>
            <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200 text-center">
              <div class="text-2xl font-bold text-orange-600">{{ caloriesBurned }}</div>
              <div class="text-sm text-gray-500">消耗卡路里</div>
            </div>
            <div class="bg-white rounded-lg shadow-sm p-6 border border-gray-200 text-center">
              <div class="text-2xl font-bold text-purple-600">{{ currentStreak }}</div>
              <div class="text-sm text-gray-500">连续天数</div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">最近活动</h3>
            </div>
            <div class="p-6">
              <div v-if="recentActivities.length === 0" class="text-center py-8">
                <i class="el-icon-time text-gray-300 text-4xl mb-3"></i>
                <p class="text-gray-500">还没有训练记录</p>
                <p class="text-sm text-gray-400 mt-1">开始您的第一次训练吧！</p>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="activity in recentActivities"
                  :key="activity.id"
                  class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                >
                  <div class="flex items-center">
                    <div class="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                      <i class="el-icon-sport text-primary-600"></i>
                    </div>
                    <div class="ml-4">
                      <div class="font-medium text-gray-900">{{ activity.type }}</div>
                      <div class="text-sm text-gray-500">{{ formatDate(activity.date) }}</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm font-medium text-gray-900">{{ activity.duration }} 分钟</div>
                    <div class="text-xs text-gray-500">{{ activity.calories }} 卡路里</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Progress Chart -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">训练趋势</h3>
            </div>
            <div class="p-6">
              <div class="h-64 flex items-center justify-center text-gray-400">
                <div class="text-center">
                  <i class="el-icon-data-line text-4xl mb-2"></i>
                  <p>训练趋势图表</p>
                  <p class="text-sm mt-1">显示最近30天的训练数据</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Achievements -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">成就徽章</h3>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-3 md:grid-cols-6 gap-4">
                <div
                  v-for="achievement in achievements"
                  :key="achievement.id"
                  class="text-center"
                  :class="{ 'opacity-50': !achievement.earned }"
                >
                  <div class="w-12 h-12 mx-auto mb-2 rounded-full flex items-center justify-center"
                       :class="achievement.earned ? 'bg-yellow-100' : 'bg-gray-100'">
                    <i class="text-lg" :class="[achievement.icon, achievement.earned ? 'text-yellow-600' : 'text-gray-400']"></i>
                  </div>
                  <div class="text-xs text-gray-600">{{ achievement.name }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Dialog -->
    <el-dialog
      title="编辑个人资料"
      v-model="showEditProfile"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="profileForm" :rules="profileRules" ref="profileFormRef" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="profileForm.name" placeholder="输入您的姓名"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="profileForm.email" placeholder="输入您的邮箱"></el-input>
        </el-form-item>
        <el-form-item label="身高" prop="height">
          <el-input-number
            v-model="profileForm.height"
            :min="100"
            :max="250"
            placeholder="身高(cm)"
          ></el-input-number>
          <span class="ml-2 text-gray-500">cm</span>
        </el-form-item>
        <el-form-item label="体重" prop="weight">
          <el-input-number
            v-model="profileForm.weight"
            :min="30"
            :max="200"
            placeholder="体重(kg)"
          ></el-input-number>
          <span class="ml-2 text-gray-500">kg</span>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number
            v-model="profileForm.age"
            :min="10"
            :max="100"
            placeholder="年龄"
          ></el-input-number>
          <span class="ml-2 text-gray-500">岁</span>
        </el-form-item>
        <el-form-item label="健身水平" prop="fitnessLevel">
          <el-select v-model="profileForm.fitnessLevel" placeholder="选择健身水平" style="width: 100%">
            <el-option label="初学者" value="beginner"></el-option>
            <el-option label="中级" value="intermediate"></el-option>
            <el-option label="高级" value="advanced"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditProfile = false">取消</el-button>
          <el-button type="primary" @click="submitProfile" :loading="submitting">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Health Data Dialog -->
    <el-dialog
      title="健康数据"
      v-model="showHealthForm"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="healthForm" label-width="100px">
        <el-form-item label="当前体重">
          <el-input-number
            v-model="healthForm.weight"
            :min="30"
            :max="200"
            placeholder="体重(kg)"
          ></el-input-number>
          <span class="ml-2 text-gray-500">kg</span>
        </el-form-item>
        <el-form-item label="体脂率">
          <el-input-number
            v-model="healthForm.bodyFat"
            :min="5"
            :max="50"
            :precision="1"
            placeholder="体脂率(%)"
          ></el-input-number>
          <span class="ml-2 text-gray-500">%</span>
        </el-form-item>
        <el-form-item label="肌肉量">
          <el-input-number
            v-model="healthForm.muscleMass"
            :min="20"
            :max="100"
            :precision="1"
            placeholder="肌肉量(kg)"
          ></el-input-number>
          <span class="ml-2 text-gray-500">kg</span>
        </el-form-item>
        <el-form-item label="心率">
          <el-input-number
            v-model="healthForm.heartRate"
            :min="40"
            :max="200"
            placeholder="静息心率"
          ></el-input-number>
          <span class="ml-2 text-gray-500">bpm</span>
        </el-form-item>
        <el-form-item label="血压">
          <el-input
            v-model="healthForm.bloodPressure"
            placeholder="例如: 120/80"
          ></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="healthForm.notes"
            type="textarea"
            :rows="3"
            placeholder="其他健康信息..."
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showHealthForm = false">取消</el-button>
          <el-button type="primary" @click="submitHealthData" :loading="submitting">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { useFitnessStore } from '@/stores/fitness'
import type { User, Activity, Achievement } from '@/types'

const userStore = useUserStore()
const fitnessStore = useFitnessStore()

// State
const showEditProfile = ref(false)
const showHealthForm = ref(false)
const showSettings = ref(false)
const showPrivacySettings = ref(false)
const showAvatarUpload = ref(false)
const submitting = ref(false)

// Form refs
const profileFormRef = ref()

// Profile form
const profileForm = reactive({
  name: userStore.user?.name || '',
  email: userStore.user?.email || '',
  height: userStore.user?.height || 0,
  weight: userStore.user?.weight || 0,
  age: userStore.user?.age || 0,
  fitnessLevel: userStore.user?.fitnessLevel || 'beginner'
})

const profileRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  height: [
    { required: true, message: '请输入身高', trigger: 'blur' }
  ],
  weight: [
    { required: true, message: '请输入体重', trigger: 'blur' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' },
    { min: 10, max: 100, message: '年龄应在 10 到 100 岁之间', trigger: 'blur' }
  ]
}

// Health form
const healthForm = reactive({
  weight: userStore.user?.weight || 0,
  bodyFat: 0,
  muscleMass: 0,
  heartRate: 0,
  bloodPressure: '',
  notes: ''
})

// Computed
const totalWorkouts = computed(() => 
  fitnessStore.activities.length
)

const totalDuration = computed(() => 
  fitnessStore.activities.reduce((total, activity) => total + (activity.duration || 0), 0)
)

const caloriesBurned = computed(() => 
  fitnessStore.activities.reduce((total, activity) => total + (activity.calories || 0), 0)
)

const currentStreak = computed(() => {
  // Calculate current workout streak
  return fitnessStore.currentStreak
})

const recentActivities = computed(() => {
  return fitnessStore.activities
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .slice(0, 5)
})

const achievements = computed(() => {
  return fitnessStore.achievements
})

// Methods
const getLevelType = (level: string) => {
  switch (level) {
    case 'beginner': return 'info'
    case 'intermediate': return 'success'
    case 'advanced': return 'warning'
    default: return 'info'
  }
}

const getLevelText = (level: string) => {
  switch (level) {
    case 'beginner': return '初学者'
    case 'intermediate': return '中级'
    case 'advanced': return '高级'
    default: return '未设置'
  }
}

const formatDate = (date: Date | string | undefined) => {
  if (!date) return '未知'
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN')
}

const submitProfile = async () => {
  if (!profileFormRef.value) return
  
  try {
    await profileFormRef.value.validate()
    submitting.value = true
    
    await userStore.updateProfile(profileForm)
    ElMessage.success('个人资料更新成功')
    showEditProfile.value = false
  } catch (error) {
    if (error !== false) {
      ElMessage.error('更新个人资料失败')
    }
  } finally {
    submitting.value = false
  }
}

const submitHealthData = async () => {
  try {
    submitting.value = true
    
    await userStore.updateHealthData(healthForm)
    ElMessage.success('健康数据更新成功')
    showHealthForm.value = false
  } catch (error) {
    ElMessage.error('更新健康数据失败')
  } finally {
    submitting.value = false
  }
}

// Load data on mount
onMounted(async () => {
  try {
    await Promise.all([
      userStore.loadUserProfile(),
      fitnessStore.loadActivities(),
      fitnessStore.loadAchievements()
    ])
    
    // Initialize profile form with current user data
    if (userStore.user) {
      Object.assign(profileForm, {
        name: userStore.user.name || '',
        email: userStore.user.email || '',
        height: userStore.user.height || 0,
        weight: userStore.user.weight || 0,
        age: userStore.user.age || 0,
        fitnessLevel: userStore.user.fitnessLevel || 'beginner'
      })
    }
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
})
</script>

<style scoped>
.el-progress-bar__outer {
  background-color: #f3f4f6;
}
</style>