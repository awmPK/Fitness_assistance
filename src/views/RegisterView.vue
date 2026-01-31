<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="flex items-center justify-center mb-4">
          <div class="w-16 h-16 bg-primary-600 rounded-xl flex items-center justify-center">
            <i class="el-icon-dumbbell text-white text-2xl"></i>
          </div>
        </div>
        <h2 class="text-3xl font-bold text-gray-900 mb-2">创建账户</h2>
        <p class="text-gray-600">开始您的健身之旅</p>
      </div>

      <!-- Registration Form -->
      <div class="bg-white rounded-xl shadow-lg p-8">
        <el-form
          :model="registerForm"
          :rules="registerRules"
          ref="registerFormRef"
          @submit.prevent="handleRegister"
        >
          <el-form-item label="姓名" prop="name">
            <el-input
              v-model="registerForm.name"
              placeholder="请输入您的姓名"
              size="large"
              clearable
            >
              <template #prefix>
                <i class="el-icon-user"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="registerForm.email"
              type="email"
              placeholder="请输入您的邮箱"
              size="large"
              clearable
            >
              <template #prefix>
                <i class="el-icon-message"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入您的密码"
              size="large"
              show-password
              clearable
            >
              <template #prefix>
                <i class="el-icon-lock"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入您的密码"
              size="large"
              show-password
              clearable
            >
              <template #prefix>
                <i class="el-icon-lock"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="健身水平" prop="fitnessLevel">
            <el-select
              v-model="registerForm.fitnessLevel"
              placeholder="请选择您的健身水平"
              size="large"
              style="width: 100%"
            >
              <el-option label="初学者" value="beginner"></el-option>
              <el-option label="中级" value="intermediate"></el-option>
              <el-option label="高级" value="advanced"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-checkbox v-model="agreeToTerms">
              我已阅读并同意
              <a href="#" class="text-primary-600 hover:text-primary-500">服务条款</a>
              和
              <a href="#" class="text-primary-600 hover:text-primary-500">隐私政策</a>
            </el-checkbox>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="w-full"
              :loading="loading"
              :disabled="!agreeToTerms"
              @click="handleRegister"
            >
              创建账户
            </el-button>
          </el-form-item>
        </el-form>

        <!-- Social Registration -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">或者使用</span>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-2 gap-3">
            <button
              @click="handleSocialRegister('google')"
              class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors"
            >
              <i class="el-icon-google mr-2"></i>
              Google
            </button>
            <button
              @click="handleSocialRegister('github')"
              class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors"
            >
              <i class="el-icon-github mr-2"></i>
              GitHub
            </button>
          </div>
        </div>

        <!-- Login Link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            已有账户？
            <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
              立即登录
            </router-link>
          </p>
        </div>
      </div>

      <!-- Benefits -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">注册后可享受</h3>
        <div class="space-y-3">
          <div class="flex items-center">
            <div class="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
              <i class="el-icon-chat-line-round text-primary-600"></i>
            </div>
            <div class="ml-3">
              <div class="text-sm font-medium text-gray-900">AI健身助手</div>
              <div class="text-xs text-gray-500">智能对话，个性化建议</div>
            </div>
          </div>
          <div class="flex items-center">
            <div class="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
              <i class="el-icon-document text-primary-600"></i>
            </div>
            <div class="ml-3">
              <div class="text-sm font-medium text-gray-900">训练计划</div>
              <div class="text-xs text-gray-500">科学的训练方案</div>
            </div>
          </div>
          <div class="flex items-center">
            <div class="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
              <i class="el-icon-data-line text-primary-600"></i>
            </div>
            <div class="ml-3">
              <div class="text-sm font-medium text-gray-900">进度追踪</div>
              <div class="text-xs text-gray-500">数据可视化，见证成长</div>
            </div>
          </div>
          <div class="flex items-center">
            <div class="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
              <i class="el-icon-brain text-primary-600"></i>
            </div>
            <div class="ml-3">
              <div class="text-sm font-medium text-gray-900">记忆功能</div>
              <div class="text-xs text-gray-500">记住您的偏好和习惯</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// State
const loading = ref(false)
const agreeToTerms = ref(false)

// Form
const registerFormRef = ref()
const registerForm = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  fitnessLevel: 'beginner'
})

// Custom validator for password confirmation
const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const registerRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  fitnessLevel: [
    { required: true, message: '请选择健身水平', trigger: 'change' }
  ]
}

// Methods
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  if (!agreeToTerms.value) {
    ElMessage.warning('请先同意服务条款和隐私政策')
    return
  }
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    await userStore.register({
        email: registerForm.email,
        password: registerForm.password,
        name: registerForm.name
      })
    
    ElMessage.success('注册成功！')
    
    // 注册成功后已自动登录，直接跳转到首页
    router.push('/')
    
  } catch (error) {
    if (error !== false) {
      ElMessage.error('注册失败，请检查输入信息')
    }
  } finally {
    loading.value = false
  }
}

const handleSocialRegister = (provider: string) => {
  ElMessage.info(`${provider} 注册功能开发中...`)
}
</script>

<style scoped>
/* Custom styles for register page */
.bg-gradient-to-br {
  background: linear-gradient(135deg, #FF6B35 0%, #1E3A8A 100%);
}

.text-primary-600 {
  color: #FF6B35;
}

.text-primary-500 {
  color: #E55A2B;
}

.bg-primary-600 {
  background-color: #FF6B35;
}

.bg-primary-50 {
  background-color: #FFF5F0;
}

.bg-secondary-50 {
  background-color: #F0F4FF;
}

.border-primary-600 {
  border-color: #FF6B35;
}

.hover\:text-primary-500:hover {
  color: #E55A2B;
}

.hover\:bg-primary-50:hover {
  background-color: #FFF5F0;
}

.hover\:bg-primary-100:hover {
  background-color: #FFE5D9;
}
</style>
