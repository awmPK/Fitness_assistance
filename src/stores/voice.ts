import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useVoiceStore = defineStore('voice', () => {
  // State
  const enabled = ref(false)
  const speechEnabled = ref(true)
  const autoSpeech = ref(false)
  const isListening = ref(false)
  const isSpeaking = ref(false)
  const recognition = ref<any | null>(null)
  const synthesis = ref<SpeechSynthesis | null>(null)

  // Initialize speech recognition and synthesis
  const initializeVoice = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
      recognition.value = new SpeechRecognition()
      recognition.value.continuous = false
      recognition.value.interimResults = true
      recognition.value.lang = 'zh-CN'
      
      recognition.value.onstart = () => {
        isListening.value = true
      }
      
      recognition.value.onend = () => {
        isListening.value = false
      }
      
      recognition.value.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error)
        isListening.value = false
      }
    }
    
    if ('speechSynthesis' in window) {
      synthesis.value = window.speechSynthesis
    }
  }

  // Start voice recognition
  const startListening = (): Promise<string> => {
    return new Promise((resolve, reject) => {
      if (!recognition.value) {
        reject(new Error('Speech recognition not supported'))
        return
      }
      
      if (isListening.value) {
        recognition.value.stop()
      }
      
      let finalTranscript = ''
      
      recognition.value.onresult = (event: any) => {
        let interimTranscript = ''
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript
          if (event.results[i].isFinal) {
            finalTranscript += transcript
          } else {
            interimTranscript += transcript
          }
        }
        
        if (finalTranscript) {
          resolve(finalTranscript)
        }
      }
      
      recognition.value.start()
    })
  }

  // Stop voice recognition
  const stopListening = () => {
    if (recognition.value && isListening.value) {
      recognition.value.stop()
      isListening.value = false
    }
  }

  // Speak text
  const speak = (text: string) => {
    if (!speechEnabled.value || !synthesis.value) {
      return
    }
    
    // Stop any current speech
    synthesis.value.cancel()
    
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'zh-CN'
    utterance.rate = 0.9
    utterance.pitch = 1
    
    utterance.onstart = () => {
      isSpeaking.value = true
    }
    
    utterance.onend = () => {
      isSpeaking.value = false
    }
    
    utterance.onerror = () => {
      isSpeaking.value = false
    }
    
    synthesis.value.speak(utterance)
  }

  // Stop speaking
  const stopSpeaking = () => {
    if (synthesis.value) {
      synthesis.value.cancel()
      isSpeaking.value = false
    }
  }

  // Toggle voice input
  const toggleVoiceInput = () => {
    enabled.value = !enabled.value
    if (enabled.value) {
      initializeVoice()
    } else {
      stopListening()
      stopSpeaking()
    }
    saveSettings()
  }

  // Toggle speech output
  const toggleSpeechOutput = () => {
    speechEnabled.value = !speechEnabled.value
    if (!speechEnabled.value) {
      stopSpeaking()
    }
    saveSettings()
  }

  // Toggle auto speech
  const toggleAutoSpeech = () => {
    autoSpeech.value = !autoSpeech.value
    saveSettings()
  }

  // Save settings
  const saveSettings = () => {
    const settings = {
      enabled: enabled.value,
      speechEnabled: speechEnabled.value,
      autoSpeech: autoSpeech.value
    }
    localStorage.setItem('voice-settings', JSON.stringify(settings))
  }

  // Load settings
  const loadSettings = () => {
    try {
      const saved = localStorage.getItem('voice-settings')
      if (saved) {
        const settings = JSON.parse(saved)
        enabled.value = settings.enabled ?? false
        speechEnabled.value = settings.speechEnabled ?? true
        autoSpeech.value = settings.autoSpeech ?? false
        
        if (enabled.value) {
          initializeVoice()
        }
      }
    } catch (error) {
      console.error('Failed to load voice settings:', error)
    }
  }

  return {
    // State
    enabled,
    speechEnabled,
    autoSpeech,
    isListening,
    isSpeaking,
    
    // Actions
    initializeVoice,
    startListening,
    stopListening,
    speak,
    stopSpeaking,
    toggleVoiceInput,
    toggleSpeechOutput,
    toggleAutoSpeech,
    saveSettings,
    loadSettings
  }
})
