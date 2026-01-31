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
              <p class="text-sm text-gray-500">管理您的个人信息</p>
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
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Profile Card -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="text-center mb-6">
          <div class="relative inline-block">
            <img
              :src="userStore.user?.avatar || 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=User%20avatar%20icon%20clean%20minimalist%20design&image_size=square'"
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
          <h2 class="text-xl font-semibold text-gray-900 mt-4">{{ userStore.user?.name || '用户' }}</h2>
          <p class="text-gray-500">{{ userStore.user?.email || 'user@example.com' }}</p>
        </div>

        <div class="space-y-4">
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-600">注册时间</span>
            <span class="text-gray-900">{{ formatDate(userStore.user?.created_at) }}</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-600">最后登录</span>
            <span class="text-gray-900">{{ formatDate(userStore.user?.last_login_at) }}</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-600">身高</span>
            <span class="text-gray-900">{{ userStore.user?.height ? userStore.user.height + ' cm' : '未设置' }}</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-600">体重</span>
            <span class="text-gray-900">{{ userStore.user?.weight ? userStore.user.weight + ' kg' : '未设置' }}</span>
          </div>
          <div class="flex justify-between items-center py-2">
            <span class="text-gray-600">年龄</span>
            <span class="text-gray-900">{{ userStore.user?.age ? userStore.user.age + ' 岁' : '未设置' }}</span>
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
            @click="showChangePassword = true"
            class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg transition-colors"
          >
            <div class="flex items-center">
              <i class="el-icon-lock text-primary-600 mr-3"></i>
              <span class="text-gray-900">修改密码</span>
            </div>
            <i class="el-icon-arrow-right text-gray-400"></i>
          </button>
          <button
            @click="handleLogout"
            class="w-full flex items-center justify-between p-3 text-left hover:bg-red-50 rounded-lg transition-colors text-red-600"
          >
            <div class="flex items-center">
              <i class="el-icon-switch-button mr-3"></i>
              <span>退出登录</span>
            </div>
            <i class="el-icon-arrow-right text-gray-400"></i>
          </button>
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

    <!-- Change Password Dialog -->
    <el-dialog
      title="修改密码"
      v-model="showChangePassword"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input v-model="passwordForm.currentPassword" type="password" placeholder="输入当前密码" show-password></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" placeholder="输入新密码" show-password></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" placeholder="再次输入新密码" show-password></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showChangePassword = false">取消</el-button>
          <el-button type="primary" @click="submitPassword" :loading="submitting">
            确认修改
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { userApi } from '@/services/api'

const router = useRouter()
const userStore = useUserStore()

// State
const showEditProfile = ref(false)
const showChangePassword = ref(false)
const showAvatarUpload = ref(false)
const submitting = ref(false)

// Form refs
const profileFormRef = ref()
const passwordFormRef = ref()

// Profile form
const profileForm = reactive({
  name: '',
  email: '',
  height: 0,
  weight: 0,
  age: 0
})

const profileRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ]
}

// Password form
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: any) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// Methods
const formatDate = (date: Date | string | undefined) => {
  if (!date) return '未知'
  const d = new Date(date)
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
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

const submitPassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    await passwordFormRef.value.validate()
    submitting.value = true
    
    if (!userStore.user) {
      ElMessage.error('用户未登录')
      return
    }
    
    const res = await userApi.changePassword(
      userStore.user.user_id,
      passwordForm.currentPassword,
      passwordForm.newPassword
    )
    
    if (res.success) {
      ElMessage.success('密码修改成功')
      showChangePassword.value = false
      
      // 清空表单
      passwordForm.currentPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
    } else {
      ElMessage.error(res.message || '修改密码失败')
    }
  } catch (error: any) {
    if (error !== false) {
      const message = error.response?.data?.detail || '修改密码失败'
      ElMessage.error(message)
    }
  } finally {
    submitting.value = false
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // 用户取消
  }
}

// Load data on mount
onMounted(async () => {
  try {
    await userStore.loadUserProfile()
    
    // Initialize profile form with current user data
    if (userStore.user) {
      Object.assign(profileForm, {
        name: userStore.user.name || '',
        email: userStore.user.email || '',
        height: userStore.user.height || 0,
        weight: userStore.user.weight || 0,
        age: userStore.user.age || 0
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
