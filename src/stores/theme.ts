import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // State
  const darkMode = ref(false)
  const animations = ref(true)
  const primaryColor = ref('#FF6B35')
  const secondaryColor = ref('#1E3A8A')

  // Actions
  const toggleDarkMode = () => {
    darkMode.value = !darkMode.value
    applyTheme()
    saveSettings()
  }

  const toggleAnimations = () => {
    animations.value = !animations.value
    saveSettings()
  }

  const setPrimaryColor = (color: string) => {
    primaryColor.value = color
    applyTheme()
    saveSettings()
  }

  const setSecondaryColor = (color: string) => {
    secondaryColor.value = color
    applyTheme()
    saveSettings()
  }

  const applyTheme = () => {
    const root = document.documentElement
    
    if (darkMode.value) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
    
    // Set CSS custom properties
    root.style.setProperty('--primary-color', primaryColor.value)
    root.style.setProperty('--secondary-color', secondaryColor.value)
    
    // Apply animations
    if (animations.value) {
      root.style.setProperty('--transition-duration', '0.3s')
    } else {
      root.style.setProperty('--transition-duration', '0s')
    }
  }

  const saveSettings = () => {
    const settings = {
      darkMode: darkMode.value,
      animations: animations.value,
      primaryColor: primaryColor.value,
      secondaryColor: secondaryColor.value
    }
    localStorage.setItem('theme-settings', JSON.stringify(settings))
  }

  const loadSettings = () => {
    try {
      const saved = localStorage.getItem('theme-settings')
      if (saved) {
        const settings = JSON.parse(saved)
        darkMode.value = settings.darkMode ?? false
        animations.value = settings.animations ?? true
        primaryColor.value = settings.primaryColor ?? '#FF6B35'
        secondaryColor.value = settings.secondaryColor ?? '#1E3A8A'
        applyTheme()
      }
    } catch (error) {
      console.error('Failed to load theme settings:', error)
    }
  }

  const resetTheme = () => {
    darkMode.value = false
    animations.value = true
    primaryColor.value = '#FF6B35'
    secondaryColor.value = '#1E3A8A'
    applyTheme()
    saveSettings()
  }

  return {
    // State
    darkMode,
    animations,
    primaryColor,
    secondaryColor,
    
    // Actions
    toggleDarkMode,
    toggleAnimations,
    setPrimaryColor,
    setSecondaryColor,
    applyTheme,
    saveSettings,
    loadSettings,
    resetTheme
  }
})