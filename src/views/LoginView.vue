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
        <h2 class="text-3xl font-bold text-gray-900 mb-2">欢迎回来</h2>
        <p class="text-gray-600">登录您的 Fitness AI 账户</p>
      </div>

      <!-- Login Form -->
      <div class="bg-white rounded-xl shadow-lg p-8">
        <el-form
          :model="loginForm"
          :rules="loginRules"
          ref="loginFormRef"
          @submit.prevent="handleLogin"
        >
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="loginForm.email"
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
              v-model="loginForm.password"
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

          <div class="flex items-center justify-between mb-6">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <a href="#" class="text-sm text-primary-600 hover:text-primary-500">
              忘记密码？
            </a>
          </div>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="w-full"
              :loading="loading"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>

        <!-- Social Login -->
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
              @click="handleSocialLogin('google')"
              class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors"
            >
              <i class="el-icon-google mr-2"></i>
              Google
            </button>
            <button
              @click="handleSocialLogin('github')"
              class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors"
            >
              <i class="el-icon-github mr-2"></i>
              GitHub
            </button>
          </div>
        </div>

        <!-- Register Link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            还没有账户？
            <router-link to="/register" class="font-medium text-primary-600 hover:text-primary-500">
              立即注册
            </router-link>
          </p>
        </div>
      </div>

      <!-- Demo Account -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">体验账户</h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div>
              <div class="text-sm font-medium text-gray-900">demo@example.com</div>
              <div class="text-xs text-gray-500">密码: demo123</div>
            </div>
            <el-button
              size="small"
              @click="useDemoAccount"
            >
              使用
            </el-button>
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
const rememberMe = ref(false)

// Form
const loginFormRef = ref()
const loginForm = reactive({
  email: '',
  password: ''
})

const loginRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

// Methods
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    await userStore.login({
      email: loginForm.email,
      password: loginForm.password
    })
    
    ElMessage.success('登录成功！')
    
    // Handle remember me
    if (rememberMe.value) {
      localStorage.setItem('rememberedEmail', loginForm.email)
    } else {
      localStorage.removeItem('rememberedEmail')
    }
    
    // Redirect to home
    router.push('/')
    
  } catch (error) {
    if (error !== false) {
      ElMessage.error('登录失败，请检查邮箱和密码')
    }
  } finally {
    loading.value = false
  }
}

const handleSocialLogin = (provider: string) => {
  ElMessage.info(`${provider} 登录功能开发中...`)
}

const useDemoAccount = () => {
  loginForm.email = 'demo@example.com'
  loginForm.password = 'demo123'
  ElMessage.success('已填入体验账户信息')
}

// Load remembered email
const loadRememberedEmail = () => {
  const remembered = localStorage.getItem('rememberedEmail')
  if (remembered) {
    loginForm.email = remembered
    rememberMe.value = true
  }
}

// Initialize
loadRememberedEmail()
</script>

<style scoped>
/* Custom styles for login page */
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
</style>