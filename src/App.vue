<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo and Brand -->
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <img src="/favicon.png" alt="Logo" class="w-8 h-8 rounded-lg shadow-sm" />
            </div>
            <div class="ml-3">
              <h1 class="text-xl font-bold text-gray-900">Fitness AI</h1>
            </div>
          </div>

          <!-- Navigation Links -->
          <div class="hidden md:block">
            <div class="ml-10 flex items-baseline space-x-4">
              <router-link
                to="/"
                class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/' ? 'bg-primary-100 text-primary-700' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'"
              >
                <i class="el-icon-chat-line-round mr-1"></i>
                AI助手
              </router-link>
              <router-link
                to="/profile"
                class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/profile' ? 'bg-primary-100 text-primary-700' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'"
              >
                <i class="el-icon-user mr-1"></i>
                个人中心
              </router-link>
            </div>
          </div>

          <!-- User Menu -->
          <div class="flex items-center space-x-4">
            <!-- Voice Toggle -->
            <el-tooltip content="语音输入" placement="bottom">
              <button
                @click="toggleVoiceInput"
                class="p-2 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
                :class="{ 'bg-primary-100 text-primary-600': voiceStore.enabled }"
              >
                <i class="el-icon-microphone text-lg"></i>
              </button>
            </el-tooltip>

            <!-- Memory Toggle -->
            <el-tooltip content="记忆功能" placement="bottom">
              <button
                @click="toggleMemory"
                class="p-2 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
                :class="{ 'bg-primary-100 text-primary-600': memoryStore.enabled }"
              >
                <i class="el-icon-brain text-lg"></i>
              </button>
            </el-tooltip>

            <!-- Settings -->
            <el-dropdown trigger="click">
              <button class="p-2 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors">
                <i class="el-icon-setting text-lg"></i>
              </button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="$router.push('/profile')">
                    <i class="el-icon-user mr-2"></i>
                    个人资料
                  </el-dropdown-item>
                  <el-dropdown-item @click="showSettings = true">
                    <i class="el-icon-setting mr-2"></i>
                    应用设置
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="logout">
                    <i class="el-icon-switch-button mr-2"></i>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <div class="md:hidden border-t border-gray-200">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link
            to="/"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            :class="$route.path === '/' ? 'bg-primary-100 text-primary-700' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'"
          >
            <i class="el-icon-chat-line-round mr-2"></i>
            AI助手
          </router-link>
          <router-link
            to="/profile"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            :class="$route.path === '/profile' ? 'bg-primary-100 text-primary-700' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'"
          >
            <i class="el-icon-user mr-2"></i>
            个人中心
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1">
      <router-view />
    </main>

    <!-- Mobile Navigation -->
    <div class="md:hidden mobile-nav safe-area-bottom">
      <div class="flex">
        <router-link
          to="/"
          class="mobile-nav-item"
          :class="{ active: $route.path === '/' }"
        >
          <i class="el-icon-chat-line-round"></i>
          <span>AI助手</span>
        </router-link>
        <router-link
          to="/profile"
          class="mobile-nav-item"
          :class="{ active: $route.path === '/profile' }"
        >
          <i class="el-icon-user"></i>
          <span>个人中心</span>
        </router-link>
      </div>
    </div>

    <!-- Settings Dialog -->
    <el-dialog
      title="应用设置"
      v-model="showSettings"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="space-y-6">
        <!-- Voice Settings -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 mb-3">语音设置</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <div class="font-medium text-gray-900">语音输入</div>
                <div class="text-sm text-gray-500">启用语音转文字功能</div>
              </div>
              <el-switch
                v-model="voiceStore.enabled"
                @change="onVoiceSettingChange"
              ></el-switch>
            </div>
            <div v-if="voiceStore.enabled" class="flex items-center justify-between">
              <div>
                <div class="font-medium text-gray-900">语音输出</div>
                <div class="text-sm text-gray-500">AI回复语音播报</div>
              </div>
              <el-switch
                v-model="voiceStore.speechEnabled"
                @change="onVoiceSettingChange"
              ></el-switch>
            </div>
            <div v-if="voiceStore.enabled" class="flex items-center justify-between">
              <div>
                <div class="font-medium text-gray-900">自动语音</div>
                <div class="text-sm text-gray-500">AI回复自动语音播报</div>
              </div>
              <el-switch
                v-model="voiceStore.autoSpeech"
                @change="onVoiceSettingChange"
              ></el-switch>
            </div>
          </div>
        </div>

        <!-- Memory Settings -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 mb-3">记忆设置</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <div class="font-medium text-gray-900">记忆功能</div>
                <div class="text-sm text-gray-500">启用AI记忆功能</div>
              </div>
              <el-switch
                v-model="memoryStore.enabled"
                @change="onMemorySettingChange"
              ></el-switch>
            </div>
            <div v-if="memoryStore.enabled" class="flex items-center justify-between">
              <div>
                <div class="font-medium text-gray-900">记忆面板</div>
                <div class="text-sm text-gray-500">显示相关记忆信息</div>
              </div>
              <el-switch
                v-model="memoryStore.showPanel"
                @change="onMemorySettingChange"
              ></el-switch>
            </div>
            <div v-if="memoryStore.enabled" class="flex items-center justify-between">
              <div>
                <div class="font-medium text-gray-900">记忆数量</div>
                <div class="text-sm text-gray-500">每次显示的记忆条数</div>
              </div>
              <el-input-number
                v-model="memoryStore.maxMemories"
                :min="1"
                :max="10"
                :step="1"
                @change="onMemorySettingChange"
              ></el-input-number>
            </div>
          </div>
        </div>

        <!-- Theme Settings -->
        <div>
          <h3 class="text-lg font-semibold text-gray-900 mb-3">主题设置</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <div class="font-medium text-gray-900">深色模式</div>
                <div class="text-sm text-gray-500">启用深色主题</div>
              </div>
              <el-switch
                v-model="themeStore.darkMode"
                @change="onThemeChange"
              ></el-switch>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <div class="font-medium text-gray-900">动画效果</div>
                <div class="text-sm text-gray-500">启用页面动画</div>
              </div>
              <el-switch
                v-model="themeStore.animations"
                @change="onThemeChange"
              ></el-switch>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showSettings = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { useVoiceStore } from '@/stores/voice'
import { useMemoryStore } from '@/stores/memory'
import { useThemeStore } from '@/stores/theme'

const router = useRouter()
const userStore = useUserStore()
const voiceStore = useVoiceStore()
const memoryStore = useMemoryStore()
const themeStore = useThemeStore()

// State
const showSettings = ref(false)

// Methods
const toggleVoiceInput = () => {
  voiceStore.toggleVoiceInput()
  ElMessage.success(voiceStore.enabled ? '语音输入已开启' : '语音输入已关闭')
}

const toggleMemory = () => {
  memoryStore.toggleMemory()
  ElMessage.success(memoryStore.enabled ? '记忆功能已开启' : '记忆功能已关闭')
}

const onVoiceSettingChange = () => {
  // Settings are automatically saved via v-model
  ElMessage.success('语音设置已更新')
}

const onMemorySettingChange = () => {
  // Settings are automatically saved via v-model
  ElMessage.success('记忆设置已更新')
}

const onThemeChange = () => {
  // Settings are automatically saved via v-model
  ElMessage.success('主题设置已更新')
}

const logout = () => {
  userStore.logout()
  router.push('/login')
  ElMessage.success('已退出登录')
}

// Load settings on mount
onMounted(async () => {
  try {
    await Promise.all([
      voiceStore.loadSettings(),
      memoryStore.loadSettings(),
      themeStore.loadSettings()
    ])
  } catch (error) {
    console.error('Failed to load settings:', error)
  }
})
</script>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Router link active styles */
.router-link-active {
  font-weight: 500;
}

/* Element Plus customizations */
.el-button--primary {
  background-color: #FF6B35;
  border-color: #FF6B35;
}

.el-button--primary:hover {
  background-color: #E55A2B;
  border-color: #E55A2B;
}

.el-button--primary:focus {
  background-color: #E55A2B;
  border-color: #E55A2B;
}
</style>