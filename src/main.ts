import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'
import './styles/responsive.css'

// Import stores
import { useUserStore } from './stores/user'
import { useChatStore } from './stores/chat'
import { useVoiceStore } from './stores/voice'
import { useMemoryStore } from './stores/memory'
import { useThemeStore } from './stores/theme'

// Import MemOS config
import { getMemosConfig, isMemOSEnabled } from './config/memos'

// Import icons
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// Create app
const app = createApp(App)

// Create pinia instance
const pinia = createPinia()

// Register Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// Use plugins
app.use(pinia)
app.use(router)
app.use(ElementPlus)

// Initialize stores
const userStore = useUserStore()
const chatStore = useChatStore()
const voiceStore = useVoiceStore()
const memoryStore = useMemoryStore()
const themeStore = useThemeStore()

// Initialize application
async function initializeApp() {
  try {
    // Load user data if authenticated
    const token = localStorage.getItem('token')
    if (token) {
      await userStore.loadUser()
    }
    
    // Load settings
    await Promise.all([
      voiceStore.loadSettings(),
      memoryStore.loadSettings(),
      themeStore.loadSettings()
    ])
    
    // Apply theme
    themeStore.applyTheme()
    
    // Initialize MemOS if enabled
    if (isMemOSEnabled()) {
      const memosConfig = getMemosConfig()
      chatStore.initializeMemOS({
        apiKey: memosConfig.apiKey,
        baseURL: memosConfig.baseURL
      })
      console.log('MemOS integration enabled')
    }
    
  } catch (error) {
    console.error('Failed to initialize app:', error)
    // Clear invalid token
    localStorage.removeItem('token')
  }
}

// Mount app
app.mount('#app')

// Initialize app data
initializeApp()

// Handle app errors
app.config.errorHandler = (error, instance, info) => {
  console.error('App error:', error, info)
}

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason)
})

// Service worker registration (for PWA support)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').then(
      (registration) => {
        console.log('SW registered: ', registration)
      },
      (error) => {
        console.log('SW registration failed: ', error)
      }
    )
  })
}